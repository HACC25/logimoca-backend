"""
Build occupation → program associations using two-stage vector matching.

Stage 1: Map occupations to pathways (887 occupations × 29 pathways)
Stage 2: Map occupations to programs within matched pathways

Uses local sentence-transformers for embeddings (no API costs).
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.db.session import session_scope
from src.models import (
    OnetOccupation, Pathway, Sector, Program, VectorChunk,
    InterestMatchedJob
)
from sqlalchemy import select
from sqlalchemy.orm import configure_mappers

# Ensure all mappers are configured
configure_mappers()


_model_cache = {"local": None}


def get_local_model():
    """Get or create the sentence-transformers model."""
    global _model_cache
    if _model_cache["local"] is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise RuntimeError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            ) from e
        print("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
        _model_cache["local"] = SentenceTransformer("all-MiniLM-L6-v2")
    return _model_cache["local"]


def embed_texts_local(texts: List[str], pad_to: int = 1024) -> np.ndarray:
    """
    Generate embeddings for a list of texts using local model.
    Pads to 1024 dimensions to match existing program embeddings.
    """
    model = get_local_model()
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    # Pad to match program embedding dimensions
    padded = []
    for emb in embeddings:
        vec = emb.astype(float)
        if len(vec) < pad_to:
            vec = np.pad(vec, (0, pad_to - len(vec)))
        elif len(vec) > pad_to:
            vec = vec[:pad_to]
        padded.append(vec)
    
    return np.array(padded)


def cosine_similarity_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity between rows of A and rows of B.
    Returns matrix of shape (len(A), len(B)).
    """
    # Normalize rows
    A_norm = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-8)
    B_norm = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-8)
    return A_norm @ B_norm.T


@dataclass
class PathwayInfo:
    id: str
    name: str
    sector_name: str
    text_for_embedding: str


@dataclass
class OccupationInfo:
    occ_code: str
    title: str
    description: str
    text_for_embedding: str


def stage1_embed_pathways(db) -> Tuple[List[PathwayInfo], np.ndarray]:
    """
    Stage 1a: Create embeddings for all pathways.
    Returns (pathway_info_list, embeddings_matrix).
    """
    print("\n" + "="*60)
    print("STAGE 1a: Embedding Pathways")
    print("="*60)
    
    pathways = db.query(Pathway).all()
    pathway_infos: List[PathwayInfo] = []
    
    for p in pathways:
        sector = db.query(Sector).filter_by(id=p.sector_id).first()
        sector_name = sector.name if sector else "Unknown"
        
        # Create rich text for embedding
        text = f"Pathway: {p.name}\nSector: {sector_name}"
        if p.description:
            text += f"\nDescription: {p.description}"
        
        pathway_infos.append(PathwayInfo(
            id=p.id,
            name=p.name,
            sector_name=sector_name,
            text_for_embedding=text
        ))
    
    print(f"Found {len(pathway_infos)} pathways")
    texts = [pi.text_for_embedding for pi in pathway_infos]
    embeddings = embed_texts_local(texts)
    
    print(f"Generated embeddings: {embeddings.shape}")
    return pathway_infos, embeddings


def stage1_embed_occupations(db) -> Tuple[List[OccupationInfo], np.ndarray]:
    """
    Stage 1b: Create embeddings for all occupations from RIASEC matching.
    Returns (occupation_info_list, embeddings_matrix).
    """
    print("\n" + "="*60)
    print("STAGE 1b: Embedding Occupations")
    print("="*60)
    
    # Get all unique occupation codes from interest matching
    unique_codes = db.query(InterestMatchedJob.occ_code).distinct().all()
    unique_codes = [code[0] for code in unique_codes]
    
    print(f"Found {len(unique_codes)} unique occupations from RIASEC matching")
    
    occupation_infos: List[OccupationInfo] = []
    
    for occ_code in unique_codes:
        occ = db.query(OnetOccupation).filter_by(onet_code=occ_code).first()
        if not occ:
            continue
        
        # Create rich text for embedding
        text = f"Occupation: {occ.title}"
        if occ.description:
            # Truncate long descriptions
            desc = occ.description[:500] if len(occ.description) > 500 else occ.description
            text += f"\nDescription: {desc}"
        
        occupation_infos.append(OccupationInfo(
            occ_code=occ.onet_code,
            title=occ.title,
            description=occ.description or "",
            text_for_embedding=text
        ))
    
    print(f"Processing {len(occupation_infos)} occupations")
    texts = [oi.text_for_embedding for oi in occupation_infos]
    embeddings = embed_texts_local(texts)
    
    print(f"Generated embeddings: {embeddings.shape}")
    return occupation_infos, embeddings


def stage1_map_occupations_to_pathways(
    occupation_infos: List[OccupationInfo],
    occupation_embeddings: np.ndarray,
    pathway_infos: List[PathwayInfo],
    pathway_embeddings: np.ndarray,
    top_k: int = 5,
    threshold: float = 0.25
) -> Dict[str, List[Tuple[str, float]]]:
    """
    Stage 1c: Compute occupation → pathway mappings using cosine similarity.
    Returns dict: {occ_code: [(pathway_id, score), ...]}
    """
    print("\n" + "="*60)
    print("STAGE 1c: Mapping Occupations to Pathways")
    print("="*60)
    
    # Compute similarity matrix: (occupations × pathways)
    print("Computing cosine similarity matrix...")
    sim_matrix = cosine_similarity_matrix(occupation_embeddings, pathway_embeddings)
    print(f"Similarity matrix shape: {sim_matrix.shape}")
    
    # For each occupation, find top-k pathways above threshold
    occ_to_pathways: Dict[str, List[Tuple[str, float]]] = {}
    
    for i, occ_info in enumerate(occupation_infos):
        scores = sim_matrix[i]
        
        # Get top-k pathway indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        # Filter by threshold
        matches = []
        for idx in top_indices:
            score = float(scores[idx])
            if score >= threshold:
                pathway_id = pathway_infos[idx].id
                matches.append((pathway_id, score))
        
        if matches:
            occ_to_pathways[occ_info.occ_code] = matches
    
    print(f"\nMapping Results:")
    print(f"  Occupations with pathway matches: {len(occ_to_pathways)}")
    print(f"  Average pathways per occupation: {np.mean([len(v) for v in occ_to_pathways.values()]):.1f}")
    
    # Show sample
    print("\nSample mappings:")
    for occ_code, pathways in list(occ_to_pathways.items())[:3]:
        occ_title = next((o.title for o in occupation_infos if o.occ_code == occ_code), "?")
        print(f"\n  {occ_code}: {occ_title}")
        for pw_id, score in pathways:
            pw_name = next((p.name for p in pathway_infos if p.id == pw_id), "?")
            print(f"    → {pw_name} (score: {score:.3f})")
    
    return occ_to_pathways


def stage2_map_occupations_to_programs(
    db,
    occupation_infos: List[OccupationInfo],
    occupation_embeddings: np.ndarray,
    occ_to_pathways: Dict[str, List[Tuple[str, float]]],
    threshold: float = 0.30,
    max_programs_per_occ: int = 20
) -> Dict[str, List[Tuple[str, float]]]:
    """
    Stage 2: Map occupations to programs within their matched pathways.
    Returns dict: {occ_code: [(program_id, score), ...]}
    """
    print("\n" + "="*60)
    print("STAGE 2: Mapping Occupations to Programs")
    print("="*60)
    
    # Load all program embeddings from vector_chunks
    print("Loading program embeddings from vector_chunks...")
    chunks = db.execute(
        select(VectorChunk.chunk_source_id, VectorChunk.chunk_embedding)
        .where(VectorChunk.chunk_source_type == 'program')
    ).fetchall()
    
    program_id_to_embedding = {
        chunk[0]: np.array(chunk[1], dtype=float)
        for chunk in chunks
    }
    print(f"Loaded {len(program_id_to_embedding)} program embeddings")
    
    # Load program → pathway mappings
    print("Loading program → pathway mappings...")
    programs = db.query(Program).all()
    program_to_pathway = {p.id: p.pathway_id for p in programs}
    
    # Build associations
    occ_to_programs: Dict[str, List[Tuple[str, float]]] = {}
    total_comparisons = 0
    
    for i, occ_info in enumerate(occupation_infos):
        occ_code = occ_info.occ_code
        
        # Get matched pathways for this occupation
        if occ_code not in occ_to_pathways:
            continue
        
        matched_pathways = [pw_id for pw_id, _ in occ_to_pathways[occ_code]]
        
        # Find programs in these pathways
        candidate_programs = [
            (prog_id, emb)
            for prog_id, emb in program_id_to_embedding.items()
            if program_to_pathway.get(prog_id) in matched_pathways
        ]
        
        if not candidate_programs:
            continue
        
        total_comparisons += len(candidate_programs)
        
        # Compute similarity to each candidate program
        occ_emb = occupation_embeddings[i]
        scores = []
        
        for prog_id, prog_emb in candidate_programs:
            # Cosine similarity
            norm_occ = np.linalg.norm(occ_emb) + 1e-8
            norm_prog = np.linalg.norm(prog_emb) + 1e-8
            score = float(np.dot(occ_emb, prog_emb) / (norm_occ * norm_prog))
            
            if score >= threshold:
                scores.append((prog_id, score))
        
        # Sort by score and take top-k
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:max_programs_per_occ]
        
        if scores:
            occ_to_programs[occ_code] = scores
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(occupation_infos)} occupations...")
    
    print(f"\nMapping Results:")
    print(f"  Total comparisons: {total_comparisons:,}")
    print(f"  Occupations with program matches: {len(occ_to_programs)}")
    print(f"  Average programs per occupation: {np.mean([len(v) for v in occ_to_programs.values()]):.1f}")
    
    # Show sample
    print("\nSample mappings:")
    for occ_code, programs in list(occ_to_programs.items())[:3]:
        occ_title = next((o.title for o in occupation_infos if o.occ_code == occ_code), "?")
        print(f"\n  {occ_code}: {occ_title}")
        for prog_id, score in programs[:5]:
            print(f"    → {prog_id} (score: {score:.3f})")
    
    return occ_to_programs


def stage3_populate_association_table(
    db,
    occ_to_programs: Dict[str, List[Tuple[str, float]]],
    dry_run: bool = False
) -> int:
    """
    Stage 3: Populate program_occupation_association table.
    Returns number of associations created.
    """
    print("\n" + "="*60)
    print("STAGE 3: Populating Association Table")
    print("="*60)
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No database changes will be made")
    
    from src.models.public_schema.associations import program_occupation_association
    from sqlalchemy import insert
    
    # Clear existing associations (if any)
    if not dry_run:
        print("Clearing existing associations...")
        db.execute(program_occupation_association.delete())
    
    # Prepare batch insert
    associations = []
    for occ_code, programs in occ_to_programs.items():
        for prog_id, score in programs:
            associations.append({
                "program_id": prog_id,
                "occupation_onet_code": occ_code,  # Must match the column name in the table
                # Store score in metadata if the table supports it
                # For now we'll just create the association
            })
    
    print(f"Prepared {len(associations)} associations")
    
    if not dry_run:
        # Batch insert
        print("Inserting into database...")
        db.execute(insert(program_occupation_association), associations)
        db.commit()
        print("✅ Associations committed to database")
    else:
        print("✅ Dry run complete - no changes made")
    
    return len(associations)


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Build occupation → program associations via two-stage vector matching'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview results without writing to database'
    )
    parser.add_argument(
        '--pathway-threshold',
        type=float,
        default=0.25,
        help='Minimum similarity for occupation → pathway match (default: 0.25)'
    )
    parser.add_argument(
        '--program-threshold',
        type=float,
        default=0.30,
        help='Minimum similarity for occupation → program match (default: 0.30)'
    )
    parser.add_argument(
        '--max-programs',
        type=int,
        default=20,
        help='Maximum programs per occupation (default: 20)'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("🚀 OCCUPATION → PROGRAM ASSOCIATION BUILDER")
    print("="*60)
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Pathway threshold: {args.pathway_threshold}")
    print(f"Program threshold: {args.program_threshold}")
    print(f"Max programs per occupation: {args.max_programs}")
    print("="*60)
    
    try:
        with session_scope() as db:
            # Stage 1: Embed and map pathways
            pathway_infos, pathway_embeddings = stage1_embed_pathways(db)
            occupation_infos, occupation_embeddings = stage1_embed_occupations(db)
            occ_to_pathways = stage1_map_occupations_to_pathways(
                occupation_infos,
                occupation_embeddings,
                pathway_infos,
                pathway_embeddings,
                top_k=5,
                threshold=args.pathway_threshold
            )
            
            # Stage 2: Map to programs
            occ_to_programs = stage2_map_occupations_to_programs(
                db,
                occupation_infos,
                occupation_embeddings,
                occ_to_pathways,
                threshold=args.program_threshold,
                max_programs_per_occ=args.max_programs
            )
            
            # Stage 3: Populate table
            total_associations = stage3_populate_association_table(
                db,
                occ_to_programs,
                dry_run=args.dry_run
            )
            
            # Final summary
            print("\n" + "="*60)
            print("📊 FINAL SUMMARY")
            print("="*60)
            print(f"Pathways embedded: {len(pathway_infos)}")
            print(f"Occupations embedded: {len(occupation_infos)}")
            print(f"Occupations matched to pathways: {len(occ_to_pathways)}")
            print(f"Occupations matched to programs: {len(occ_to_programs)}")
            print(f"Total associations: {total_associations}")
            print("="*60)
            
            if not args.dry_run:
                print("\n✅ Association table populated successfully!")
            else:
                print("\n⚠️  This was a DRY RUN - run without --dry-run to commit")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
