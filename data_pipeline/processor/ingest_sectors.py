"""
Ingest sectors and pathways from structured_career_pathways.json into the database.

This script populates:
- sectors table (career pathway industry domains)
- pathways table (specific career pathways within sectors)

Usage:
    python -m data_pipeline.processor.ingest_sectors
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.exc import IntegrityError
from src.db.session import session_scope
from src.models.public_schema.sector import Sector
from src.models.public_schema.pathway import Pathway


def load_json_data(filepath: Path) -> List[Dict]:
    """Load structured career pathways JSON data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def ingest_sectors_and_pathways(data: List[Dict], dry_run: bool = False) -> Dict[str, int]:
    """
    Ingest sectors and pathways from structured JSON data.
    
    Args:
        data: List of sector dictionaries from JSON
        dry_run: If True, don't commit to database
        
    Returns:
        Dictionary with counts of inserted/updated records
    """
    stats = {
        'sectors_inserted': 0,
        'sectors_updated': 0,
        'pathways_inserted': 0,
        'pathways_updated': 0,
        'sectors_skipped': 0,
        'pathways_skipped': 0,
    }
    
    with session_scope() as db:
        for sector_data in data:
            sector_id = sector_data.get('id')
            sector_name = sector_data.get('sector_name')
            pathway_url = sector_data.get('pathway_url', '')
            
            if not sector_id or not sector_name:
                print(f"⚠️  Skipping sector with missing id or name: {sector_data}")
                stats['sectors_skipped'] += 1
                continue
            
            # Check if sector exists
            existing_sector = db.query(Sector).filter(Sector.id == sector_id).first()
            
            # Use sector_name as description for now (can be enhanced later)
            description = f"{sector_name} - Career pathways and programs in this sector."
            
            if existing_sector:
                # Update existing sector
                existing_sector.name = sector_name
                existing_sector.description = description
                existing_sector.pathway_url = pathway_url
                print(f"🔄 Updated sector: {sector_id} - {sector_name}")
                stats['sectors_updated'] += 1
            else:
                # Insert new sector
                new_sector = Sector(
                    id=sector_id,
                    name=sector_name,
                    description=description,
                    pathway_url=pathway_url,
                    icon_url=None  # Can be added later
                )
                db.add(new_sector)
                print(f"✅ Inserted sector: {sector_id} - {sector_name}")
                stats['sectors_inserted'] += 1
            
            # Process pathways for this sector
            pathways = sector_data.get('pathways', [])
            for pathway_data in pathways:
                pathway_id = pathway_data.get('id')
                pathway_name = pathway_data.get('name')
                pathway_description = pathway_data.get('description', '')
                pathway_url_data = pathway_data.get('pathway_url', '')
                
                if not pathway_id or not pathway_name:
                    print(f"  ⚠️  Skipping pathway with missing id or name: {pathway_data.get('name', 'unknown')}")
                    stats['pathways_skipped'] += 1
                    continue
                
                # Check if pathway exists
                existing_pathway = db.query(Pathway).filter(Pathway.id == pathway_id).first()
                
                if existing_pathway:
                    # Update existing pathway
                    existing_pathway.name = pathway_name
                    existing_pathway.description = pathway_description
                    existing_pathway.pathway_url = pathway_url_data
                    existing_pathway.sector_id = sector_id
                    print(f"  🔄 Updated pathway: {pathway_id} - {pathway_name}")
                    stats['pathways_updated'] += 1
                else:
                    # Insert new pathway
                    new_pathway = Pathway(
                        id=pathway_id,
                        name=pathway_name,
                        description=pathway_description,
                        pathway_url=pathway_url_data,
                        sector_id=sector_id
                    )
                    db.add(new_pathway)
                    print(f"  ✅ Inserted pathway: {pathway_id} - {pathway_name}")
                    stats['pathways_inserted'] += 1
        
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
        description='Ingest sectors and pathways from structured JSON data'
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
    stats = ingest_sectors_and_pathways(data, dry_run=args.dry_run)
    
    # Print summary
    print("\n" + "="*60)
    print("📈 INGESTION SUMMARY")
    print("="*60)
    print(f"Sectors inserted:   {stats['sectors_inserted']}")
    print(f"Sectors updated:    {stats['sectors_updated']}")
    print(f"Sectors skipped:    {stats['sectors_skipped']}")
    print(f"Pathways inserted:  {stats['pathways_inserted']}")
    print(f"Pathways updated:   {stats['pathways_updated']}")
    print(f"Pathways skipped:   {stats['pathways_skipped']}")
    print("="*60)
    
    if args.dry_run:
        print("\n⚠️  This was a DRY RUN - no changes were committed")
    else:
        print("\n✅ Ingestion complete!")


if __name__ == "__main__":
    main()
