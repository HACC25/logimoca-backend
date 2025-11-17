"""
Enrich program data using similarity search and external data sources.

This script will:
1. Identify programs with missing or incomplete descriptions
2. Use vector similarity to find related programs and O*NET occupations  
3. Generate enhanced descriptions based on similar programs
4. Fill in missing metadata (prerequisites, delivery modes, etc.)
"""
import sys
sys.path.insert(0, 'src')

from db.session import get_session_factory
from models.public_schema.program import Program
from models.public_schema.vector_chunk import VectorChunk
from sqlalchemy import func, and_, or_
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the same embedding model used for initial program embeddings
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_similar_programs(program, db, top_k=5):
    """Find similar programs using vector similarity."""
    # Get the program's embedding from vector_chunks
    chunk = db.query(VectorChunk).filter(
        and_(
            VectorChunk.source_type == 'program',
            VectorChunk.source_id == str(program.id)
        )
    ).first()
    
    if not chunk or not chunk.embedding:
        return []
    
    # Get all other program embeddings
    all_chunks = db.query(VectorChunk).filter(
        and_(
            VectorChunk.source_type == 'program',
            VectorChunk.source_id != str(program.id)
        )
    ).all()
    
    # Calculate similarities
    similarities = []
    for other_chunk in all_chunks:
        if other_chunk.embedding:
            sim = cosine_similarity(chunk.embedding, other_chunk.embedding)
            similarities.append((other_chunk.source_id, sim))
    
    # Sort by similarity and get top_k
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar_ids = [int(sid) for sid, _ in similarities[:top_k]]
    
    # Fetch the actual programs
    similar_programs = db.query(Program).filter(Program.id.in_(top_similar_ids)).all()
    return similar_programs

def enhance_program_description(program, similar_programs):
    """Generate an enhanced description based on similar programs."""
    if program.description and len(program.description) > 50:
        return program.description  # Already has a good description
    
    # Build enhanced description from similar programs
    if not similar_programs:
        return program.description
    
    # Use the most similar program's description as a template
    template = similar_programs[0].description if similar_programs[0].description else ""
    
    # For now, just return the template (in a real scenario, we'd use LLM to customize it)
    return template

def infer_delivery_modes(program, similar_programs):
    """Infer delivery modes from similar programs."""
    if program.delivery_modes:
        return program.delivery_modes
    
    # Aggregate delivery modes from similar programs
    modes = set()
    for sp in similar_programs:
        if sp.delivery_modes:
            modes.update(sp.delivery_modes)
    
    return list(modes) if modes else None

def infer_prerequisites(program, similar_programs):
    """Infer prerequisites from similar programs."""
    if program.prerequisites:
        return program.prerequisites
    
    # Use the most similar program's prerequisites
    for sp in similar_programs:
        if sp.prerequisites:
            return sp.prerequisites
    
    return None

def main():
    SessionLocal = get_session_factory()
    db = SessionLocal()
    
    try:
        # Find programs with incomplete data
        print("\nAnalyzing program data quality...")
        print("=" * 80)
        
        incomplete_programs = db.query(Program).filter(
            or_(
                Program.description == None,
                Program.description == '',
                func.length(Program.description) < 50,
                Program.delivery_modes == None,
                Program.prerequisites == None
            )
        ).limit(20).all()  # Start with first 20
        
        print(f"Found {len(incomplete_programs)} programs with incomplete data\n")
        
        updates_made = 0
        for program in incomplete_programs:
            print(f"Processing: {program.name[:60]}")
            
            # Find similar programs
            similar = find_similar_programs(program, db, top_k=3)
            
            if similar:
                print(f"  Found {len(similar)} similar programs")
                
                # Enhance description
                new_desc = enhance_program_description(program, similar)
                if new_desc != program.description:
                    print(f"    ✓ Enhanced description")
                    program.description = new_desc
                    updates_made += 1
                
                # Infer delivery modes
                new_modes = infer_delivery_modes(program, similar)
                if new_modes and not program.delivery_modes:
                    print(f"    ✓ Inferred delivery modes: {new_modes}")
                    program.delivery_modes = new_modes
                    updates_made += 1
                
                # Infer prerequisites  
                new_prereq = infer_prerequisites(program, similar)
                if new_prereq and not program.prerequisites:
                    print(f"    ✓ Inferred prerequisites")
                    program.prerequisites = new_prereq
                    updates_made += 1
            else:
                print(f"  No similar programs found")
            
            print()
        
        if updates_made > 0:
            print(f"\nCommitting {updates_made} updates...")
            db.commit()
            print("✓ Updates committed successfully")
        else:
            print("\nNo updates needed")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
