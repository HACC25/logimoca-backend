"""
Populate the public.occupation table with O*NET occupations.

This script:
1. Queries unique occupations from riasec.interest_matched_job
2. Fetches corresponding data from onet.occupation_data
3. Populates public.occupation table with enriched occupation data
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text, select
from sqlalchemy.dialects.postgresql import insert
from src.db.session import get_session_factory
from src.models.riasec_schema.interest_matched_job import InterestMatchedJob
from src.models.onet_schema.onet_occupation import OnetOccupation
from src.models.public_schema.occupation import Occupation


def populate_occupations(dry_run: bool = False):
    """
    Populate the occupation table from InterestMatchedJob and OnetOccupation data.
    
    Args:
        dry_run: If True, only shows what would be inserted without committing
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("🔄 POPULATING PUBLIC.OCCUPATION TABLE")
        print("=" * 60)
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print()
        
        # Step 1: Get unique occupation codes from InterestMatchedJob
        print("Step 1: Fetching unique occupation codes from InterestMatchedJob...")
        unique_codes = db.query(InterestMatchedJob.occ_code).distinct().all()
        occupation_codes = [code[0] for code in unique_codes]
        print(f"  Found {len(occupation_codes)} unique occupation codes")
        print()
        
        # Step 2: Get O*NET data for these occupations
        print("Step 2: Fetching O*NET occupation data...")
        onet_occupations = db.query(OnetOccupation).filter(
            OnetOccupation.onet_code.in_(occupation_codes)
        ).all()
        
        print(f"  Found O*NET data for {len(onet_occupations)} occupations")
        
        if len(onet_occupations) < len(occupation_codes):
            missing = set(occupation_codes) - {occ.onet_code for occ in onet_occupations}
            print(f"  ⚠️  Warning: {len(missing)} codes not found in O*NET data")
            if len(missing) <= 10:
                print(f"     Missing: {missing}")
        print()
        
        # Step 3: Prepare occupation records
        print("Step 3: Preparing occupation records...")
        occupation_records = []
        
        for onet_occ in onet_occupations:
            # Extract job zone from description if available
            # O*NET job zones range from 1 (little/no prep) to 5 (extensive prep)
            job_zone = 3  # Default to middle value if not determinable
            
            # Build O*NET URL
            onet_url = f"https://www.onetonline.org/link/summary/{onet_occ.onet_code}"
            
            record = {
                "onet_code": onet_occ.onet_code,
                "median_annual_wage": None,  # To be filled from external APIs later
                "employment_outlook": "Unknown",  # To be filled from O*NET data later
                "job_zone": job_zone,
                "interest_codes": [],  # To be populated from RIASEC analysis
                "interest_scores": {},  # To be populated from RIASEC analysis
                "top_skills": [],  # To be populated from O*NET skills analysis
                "onet_url": onet_url,
                "last_updated": datetime.now(),
            }
            occupation_records.append(record)
        
        print(f"  Prepared {len(occupation_records)} occupation records")
        print()
        
        # Sample records
        if occupation_records:
            print("Sample records (first 3):")
            for i, rec in enumerate(occupation_records[:3], 1):
                print(f"  {i}. {rec['onet_code']} (job_zone={rec['job_zone']})")
            print()
        
        if dry_run:
            print("✅ DRY RUN COMPLETE - No changes made")
            return len(occupation_records)
        
        # Step 4: Insert/update records (upsert)
        print("Step 4: Inserting into occupation table...")
        
        # Use PostgreSQL's ON CONFLICT to handle existing records
        stmt = insert(Occupation).values(occupation_records)
        stmt = stmt.on_conflict_do_update(
            index_elements=['onet_code'],
            set_={
                'job_zone': stmt.excluded.job_zone,
                'employment_outlook': stmt.excluded.employment_outlook,
            }
        )
        
        db.execute(stmt)
        db.commit()
        
        print(f"✅ Successfully inserted/updated {len(occupation_records)} occupations")
        print()
        
        # Verify
        count = db.query(Occupation).count()
        print(f"Total occupations in table: {count}")
        
        return len(occupation_records)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


def main():
    """Main entry point with CLI argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Populate public.occupation table from O*NET and RIASEC data"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be inserted without committing changes"
    )
    
    args = parser.parse_args()
    
    try:
        count = populate_occupations(dry_run=args.dry_run)
        
        if not args.dry_run:
            print()
            print("=" * 60)
            print(f"🎉 POPULATION COMPLETE: {count} occupations")
            print("=" * 60)
            print()
            print("Next steps:")
            print("  1. Run build_occupation_associations.py to create program links")
            print("  2. Optionally update occupation fields with wage/outlook data")
    
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
