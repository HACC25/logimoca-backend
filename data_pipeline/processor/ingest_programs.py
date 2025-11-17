"""
Ingest programs from structured_career_pathways.json into the database.

This script populates:
- programs table (training programs from pathways)

Note: This is a basic ingestion that creates program records with essential fields.
Fields like duration_years, cost_per_credit, etc. will be populated later via:
- Heuristic data scraping
- LLM extraction
- Vector similarity matching

Usage:
    python -m data_pipeline.processor.ingest_programs
"""

import json
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.exc import IntegrityError
from src.db.session import session_scope
from src.models.public_schema.program import Program
from src.models.public_schema.pathway import Pathway
from src.models.public_schema.institution import Institution


def load_json_data(filepath: Path) -> List[Dict]:
    """Load structured career pathways JSON data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_program_id(program_name: str, institution_id: str) -> str:
    """
    Generate a unique program ID from name and institution.
    Uses hash to keep ID length manageable.
    
    Args:
        program_name: Name of the program
        institution_id: ID of the institution
        
    Returns:
        Unique program ID (max 50 chars)
    """
    # Create a deterministic hash
    combined = f"{institution_id}:{program_name}".lower()
    hash_suffix = hashlib.md5(combined.encode()).hexdigest()[:8]
    
    # Clean program name for ID
    clean_name = "".join(c if c.isalnum() else "_" for c in program_name.lower())
    clean_name = clean_name[:35]  # Limit length
    
    return f"{institution_id}_{clean_name}_{hash_suffix}"


def parse_degree_type(program_name: str, description: str = "") -> str:
    """
    Infer degree type from program name or description.
    
    Returns one of: 'Certificate', 'Associate', 'Bachelor', 'Master', 'Doctorate'
    Defaults to 'Certificate' if unknown.
    """
    combined_text = f"{program_name} {description}".lower()
    
    if any(term in combined_text for term in ['doctorate', 'phd', 'ph.d', 'doctoral']):
        return 'Doctorate'
    elif any(term in combined_text for term in ['master', "master's", 'ms', 'ma', 'm.s.', 'm.a.']):
        return 'Master'
    elif any(term in combined_text for term in ['bachelor', "bachelor's", 'bs', 'ba', 'b.s.', 'b.a.', 'baccalaureate']):
        return 'Bachelor'
    elif any(term in combined_text for term in ['associate', "associate's", 'as', 'aa', 'a.s.', 'a.a.']):
        return 'Associate'
    elif any(term in combined_text for term in ['certificate', 'cert', 'certification']):
        return 'Certificate'
    else:
        # Default to Certificate for unknown types
        return 'Certificate'


def get_or_create_default_institution(db) -> str:
    """
    Get or create a default 'Unknown' institution for programs without institution data.
    
    Returns:
        Institution ID
    """
    default_id = "UH-UNKNOWN"
    existing = db.query(Institution).filter(Institution.id == default_id).first()
    
    if not existing:
        default_institution = Institution(
            id=default_id,
            name="University of Hawaiʻi - Unknown Campus",
            type="4-year",
            location="Oʻahu",
            campus="TBD",
            website_url="https://www.hawaii.edu",
            contact_email=None,
            latitude=None,
            longitude=None
        )
        db.add(default_institution)
        print(f"✅ Created default institution: {default_id}")
    
    return default_id


def ingest_programs(data: List[Dict], dry_run: bool = False) -> Dict[str, int]:
    """
    Ingest programs from structured JSON data.
    
    Args:
        data: List of sector dictionaries from JSON
        dry_run: If True, don't commit to database
        
    Returns:
        Dictionary with counts of inserted/updated records
    """
    stats = {
        'programs_inserted': 0,
        'programs_updated': 0,
        'programs_skipped': 0,
        'pathways_missing': 0,
        'duplicates_skipped': 0,
    }
    
    with session_scope() as db:
        # Ensure default institution exists
        default_institution_id = get_or_create_default_institution(db)
        
        # Track program IDs we've already processed in this session
        processed_ids = set()
        
        for sector_data in data:
            sector_id = sector_data.get('id')
            sector_name = sector_data.get('sector_name')
            
            print(f"\n📂 Processing sector: {sector_name} ({sector_id})")
            
            pathways = sector_data.get('pathways', [])
            for pathway_data in pathways:
                pathway_id = pathway_data.get('id')
                pathway_name = pathway_data.get('name')
                
                # Verify pathway exists in database
                existing_pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
                if not existing_pathway:
                    print(f"  ⚠️  Pathway not found in DB: {pathway_id} - {pathway_name}")
                    stats['pathways_missing'] += 1
                    continue
                
                programs = pathway_data.get('programs', [])
                
                if not programs:
                    print(f"  ℹ️  No programs in pathway: {pathway_name}")
                    continue
                
                print(f"  📁 Processing {len(programs)} programs in pathway: {pathway_name}")
                
                for program_data in programs:
                    # Use 'name' field (JSON has 'name', not 'program_name')
                    program_name = program_data.get('name')
                    program_id = program_data.get('id')  # Use existing ID from JSON
                    
                    if not program_name or not program_id:
                        stats['programs_skipped'] += 1
                        continue
                    
                    # Skip duplicates within the JSON (same program in multiple pathways)
                    if program_id in processed_ids:
                        stats['duplicates_skipped'] += 1
                        continue
                    
                    processed_ids.add(program_id)
                    
                    # Extract available fields from JSON
                    program_url = program_data.get('program_url', '')
                    description = program_data.get('description', '')
                    program_links = program_data.get('program_links', [])  # Array of URLs
                    
                    # For now, use default institution (can be enhanced later with institution matching)
                    institution_id = default_institution_id
                    
                    # Infer degree type
                    degree_type = parse_degree_type(program_name, description)
                    
                    # Check if program exists
                    existing_program = db.query(Program).filter(Program.id == program_id).first()
                    
                    # Default placeholder values for fields to be populated later
                    duration_years = 2.0  # Default placeholder
                    total_credits = 60  # Default placeholder
                    cost_per_credit = 350.0  # Default UH system average
                    
                    if existing_program:
                        # Update existing program
                        existing_program.name = program_name
                        existing_program.pathway_id = pathway_id
                        existing_program.institution_id = institution_id
                        existing_program.degree_type = degree_type
                        existing_program.description = description or program_name
                        existing_program.program_url = program_url
                        existing_program.program_links = program_links  # Update links
                        # Don't overwrite duration/cost if already set
                        print(f"    🔄 Updated program: {program_name[:50]}")
                        stats['programs_updated'] += 1
                    else:
                        # Insert new program
                        new_program = Program(
                            id=program_id,
                            name=program_name,
                            pathway_id=pathway_id,
                            institution_id=institution_id,
                            degree_type=degree_type,
                            duration_years=duration_years,
                            total_credits=total_credits,
                            cost_per_credit=cost_per_credit,
                            description=description or program_name,
                            program_url=program_url,
                            program_links=program_links,  # Add links array
                            prerequisites=[],
                            delivery_modes=[]
                        )
                        db.add(new_program)
                        print(f"    ✅ Inserted program: {program_name[:50]}")
                        stats['programs_inserted'] += 1
        
        if dry_run:
            print("\n🔍 DRY RUN - Rolling back changes")
            db.rollback()
        else:
            print("\n💾 Committing changes to database...")
            db.commit()
    
    return stats


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Ingest programs from structured JSON data'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without committing to database'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data_pipeline/raw/structured_career_pathways.json',
        help='Path to structured career pathways JSON file'
    )
    
    args = parser.parse_args()
    
    # Resolve file path
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = project_root / input_path
    
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)
    
    print(f"📁 Loading data from: {input_path}")
    data = load_json_data(input_path)
    print(f"📊 Found {len(data)} sectors in JSON file\n")
    
    # Ingest data
    stats = ingest_programs(data, dry_run=args.dry_run)
    
    # Print summary
    print("\n" + "="*60)
    print("📈 PROGRAMS INGESTION SUMMARY")
    print("="*60)
    print(f"Programs inserted:     {stats['programs_inserted']}")
    print(f"Programs updated:      {stats['programs_updated']}")
    print(f"Programs skipped:      {stats['programs_skipped']}")
    print(f"Duplicates skipped:    {stats['duplicates_skipped']}")
    print(f"Pathways missing:      {stats['pathways_missing']}")
    print("="*60)
    
    if stats['pathways_missing'] > 0:
        print("\n⚠️  Some pathways were not found in the database.")
        print("   Run ingest_sectors.py first to populate sectors and pathways.")
    
    if args.dry_run:
        print("\n⚠️  This was a DRY RUN - no changes were committed")
    else:
        print("\n✅ Programs ingestion complete!")
        print("\nℹ️  Note: Duration, cost, and detailed fields are placeholders.")
        print("   Run enhancement scripts later to populate with real data.")


if __name__ == "__main__":
    main()
