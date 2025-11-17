"""
Master ingestion script to populate sectors, pathways, and programs.

This script runs the ingestion pipeline in the correct order:
1. Sectors and Pathways
2. Programs

Usage:
    python -m data_pipeline.processor.ingest_all
    python -m data_pipeline.processor.ingest_all --dry-run
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_pipeline.processor.ingest_sectors import ingest_sectors_and_pathways, load_json_data
from data_pipeline.processor.ingest_programs import ingest_programs


def main():
    """Run complete ingestion pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Run complete ingestion pipeline for sectors, pathways, and programs'
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
    parser.add_argument(
        '--skip-sectors',
        action='store_true',
        help='Skip sectors/pathways ingestion (only run programs)'
    )
    parser.add_argument(
        '--skip-programs',
        action='store_true',
        help='Skip programs ingestion (only run sectors/pathways)'
    )
    
    args = parser.parse_args()
    
    # Resolve file path
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = project_root / input_path
    
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        sys.exit(1)
    
    print("="*70)
    print("🚀 STARTING COMPLETE INGESTION PIPELINE")
    print("="*70)
    print(f"📁 Input file: {input_path}")
    print(f"🔍 Dry run: {args.dry_run}")
    print("="*70)
    
    # Load data once
    print(f"\n📁 Loading data from: {input_path}")
    data = load_json_data(input_path)
    print(f"📊 Found {len(data)} sectors in JSON file")
    
    total_stats = {
        'sectors_inserted': 0,
        'sectors_updated': 0,
        'pathways_inserted': 0,
        'pathways_updated': 0,
        'programs_inserted': 0,
        'programs_updated': 0,
    }
    
    # Step 1: Ingest Sectors and Pathways
    if not args.skip_sectors:
        print("\n" + "="*70)
        print("📍 STEP 1: INGESTING SECTORS AND PATHWAYS")
        print("="*70)
        
        sector_stats = ingest_sectors_and_pathways(data, dry_run=args.dry_run)
        
        total_stats['sectors_inserted'] = sector_stats['sectors_inserted']
        total_stats['sectors_updated'] = sector_stats['sectors_updated']
        total_stats['pathways_inserted'] = sector_stats['pathways_inserted']
        total_stats['pathways_updated'] = sector_stats['pathways_updated']
        
        print("\n✅ Sectors and Pathways ingestion complete")
    else:
        print("\n⏭️  Skipping sectors and pathways ingestion")
    
    # Step 2: Ingest Programs
    if not args.skip_programs:
        print("\n" + "="*70)
        print("📍 STEP 2: INGESTING PROGRAMS")
        print("="*70)
        
        program_stats = ingest_programs(data, dry_run=args.dry_run)
        
        total_stats['programs_inserted'] = program_stats['programs_inserted']
        total_stats['programs_updated'] = program_stats['programs_updated']
        
        print("\n✅ Programs ingestion complete")
    else:
        print("\n⏭️  Skipping programs ingestion")
    
    # Final Summary
    print("\n" + "="*70)
    print("🎉 COMPLETE INGESTION SUMMARY")
    print("="*70)
    print(f"Sectors inserted:      {total_stats['sectors_inserted']}")
    print(f"Sectors updated:       {total_stats['sectors_updated']}")
    print(f"Pathways inserted:     {total_stats['pathways_inserted']}")
    print(f"Pathways updated:      {total_stats['pathways_updated']}")
    print(f"Programs inserted:     {total_stats['programs_inserted']}")
    print(f"Programs updated:      {total_stats['programs_updated']}")
    print("="*70)
    
    if args.dry_run:
        print("\n⚠️  This was a DRY RUN - no changes were committed to the database")
    else:
        print("\n✅ All data successfully ingested into the database!")
        print("\nℹ️  Next steps:")
        print("   - Run enhancement scripts to populate duration, costs, etc.")
        print("   - Use LLM/vector matching to link programs with occupations")
        print("   - Add institution matching logic")


if __name__ == "__main__":
    main()
