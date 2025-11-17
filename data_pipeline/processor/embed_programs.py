# data_pipeline/processor/embed_programs.py

"""
Chunk and embed program descriptions for semantic search.
Creates vector_chunks from existing programs table.

Uses Voyage AI for embeddings (free tier: 1M tokens/month).
Alternative: Can use sentence-transformers locally if preferred.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import requests

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.db.session import session_scope
from src.models import Program, VectorChunk


def chunk_program_text(program: Program) -> List[Dict]:
    """
    Break program into semantic chunks.
    
    Returns list of chunk dicts with:
    - text: The chunk content
    - metadata: Dict with program_id, url, etc.
    """
    chunks = []
    
    # Main description chunk
    if program.description:
        # Truncate very long descriptions
        desc_text = program.description[:2000] if len(program.description) > 2000 else program.description
        chunks.append({
            "text": f"Program: {program.name}\n\n{desc_text}",
            "metadata": {
                "program_id": program.id,
                "program_name": program.name,
                "source_url": program.program_url,
                "chunk_type": "description"
            }
        })
    
    # Links as separate context (optional)
    # if program.program_links and len(program.program_links) > 0:
    #     link_text = f"Program: {program.name}\nRelated resources:\n" + "\n".join(program.program_links[:5])
    #     chunks.append({
    #         "text": link_text,
    #         "metadata": {
    #             "program_id": program.id,
    #             "program_name": program.name,
    #             "chunk_type": "links"
    #         }
    #     })
    
    return chunks


def embed_texts_voyage(texts: List[str], api_key: str) -> List[List[float]]:
    """
    Generate embeddings using Voyage AI.
    
    Args:
        texts: List of text strings to embed
        api_key: Voyage AI API key
    
    Returns:
        List of embedding vectors
    """
    url = "https://api.voyageai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "input": texts,
        "model": "voyage-2"  # or "voyage-large-2-instruct" for better quality
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    return [item["embedding"] for item in data["data"]]


def embed_texts_local(texts: List[str], model_name: str = "all-MiniLM-L6-v2") -> List[List[float]]:
    """
    Generate embeddings using local sentence-transformers model.
    No API key needed, runs on your machine.
    
    Requires: pip install sentence-transformers
    
    Args:
        texts: List of text strings to embed
        model_name: HuggingFace model name
            - "all-MiniLM-L6-v2": Fast, 384 dims (default)
            - "all-mpnet-base-v2": Better quality, 768 dims
    
    Returns:
        List of embedding vectors
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers not installed. "
            "Install with: pip install sentence-transformers"
        )
    
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def get_embedding_function(use_local: bool = False):
    """
    Get the appropriate embedding function based on configuration.
    
    Args:
        use_local: If True, use local model. If False, use Voyage AI.
    
    Returns:
        Tuple of (embed_function, requires_api_key)
    """
    if use_local:
        return embed_texts_local, False
    else:
        return embed_texts_voyage, True


def ingest_program_embeddings(dry_run: bool = False, batch_size: int = 10, use_local: bool = False):
    """
    Create vector chunks from all programs.
    
    Args:
        dry_run: If True, don't commit to database
        batch_size: Number of texts to embed at once (Voyage supports batches)
        use_local: If True, use local sentence-transformers (no API key needed)
    """
    # Get embedding function
    embed_func, needs_api_key = get_embedding_function(use_local)
    
    voyage_api_key = None
    if needs_api_key:
        voyage_api_key = os.getenv("VOYAGE_API_KEY")
        if not voyage_api_key:
            raise ValueError(
                "VOYAGE_API_KEY not found in environment variables. "
                "Use --local flag to use local embeddings instead."
            )
    
    stats = {"chunks_created": 0, "programs_processed": 0, "errors": 0}
    
    with session_scope() as db:
        programs = db.query(Program).all()
        print(f"📊 Found {len(programs)} programs to process")
        
        if use_local:
            print("🏠 Using LOCAL sentence-transformers (no API needed)")
        else:
            print("☁️  Using VOYAGE AI embeddings")
        print(f"📦 Batch size: {batch_size}\n")
        
        # Process in batches for efficiency
        all_chunks_data = []
        all_texts = []
        
        for program in programs:
            chunks = chunk_program_text(program)
            for chunk_data in chunks:
                all_chunks_data.append(chunk_data)
                all_texts.append(chunk_data["text"])
        
        print(f"📦 Generated {len(all_chunks_data)} chunks total")
        print(f"🔄 Embedding in batches of {batch_size}...\n")
        
        # Embed in batches
        for i in range(0, len(all_texts), batch_size):
            batch_texts = all_texts[i:i+batch_size]
            batch_chunks = all_chunks_data[i:i+batch_size]
            
            try:
                print(f"  Embedding batch {i//batch_size + 1}/{(len(all_texts)-1)//batch_size + 1}...", end=" ")
                
                # Call appropriate embedding function
                if needs_api_key:
                    embeddings = embed_func(batch_texts, voyage_api_key)
                else:
                    embeddings = embed_func(batch_texts)
                
                # Create VectorChunk records
                for chunk_data, embedding in zip(batch_chunks, embeddings):
                    chunk = VectorChunk(
                        chunk_text=chunk_data["text"],
                        chunk_embedding=embedding,
                        chunk_source_type="program",
                        chunk_source_id=chunk_data["metadata"]["program_id"],
                        chunk_metadata=chunk_data["metadata"]
                    )
                    db.add(chunk)
                    stats["chunks_created"] += 1
                
                print(f"✅ {len(batch_texts)} chunks")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                stats["errors"] += 1
                continue
        
        # Count unique programs processed
        unique_programs = set(c["metadata"]["program_id"] for c in all_chunks_data)
        stats["programs_processed"] = len(unique_programs)
        
        if dry_run:
            print("\n🔍 DRY RUN - rolling back")
            db.rollback()
        else:
            print("\n💾 Committing to database...")
            db.commit()
    
    return stats


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate embeddings for program data'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without committing to database'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Number of texts to embed per API call (default: 10)'
    )
    parser.add_argument(
        '--local',
        action='store_true',
        help='Use local sentence-transformers instead of Voyage AI (no API key needed)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 PROGRAM EMBEDDING PIPELINE")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Batch size: {args.batch_size}")
    print(f"Embedding: {'Local (sentence-transformers)' if args.local else 'Voyage AI'}")
    print("=" * 60 + "\n")
    
    try:
        stats = ingest_program_embeddings(
            dry_run=args.dry_run,
            batch_size=args.batch_size,
            use_local=args.local
        )
        
        # Print summary
        print("\n" + "=" * 60)
        print("📈 EMBEDDING SUMMARY")
        print("=" * 60)
        print(f"Programs processed:    {stats['programs_processed']}")
        print(f"Chunks created:        {stats['chunks_created']}")
        print(f"Errors:                {stats['errors']}")
        print("=" * 60)
        
        if args.dry_run:
            print("\n⚠️  This was a DRY RUN - no changes were committed")
        else:
            print("\n✅ Embeddings successfully created!")
            print("\nℹ️  You can now use semantic search over program data")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
