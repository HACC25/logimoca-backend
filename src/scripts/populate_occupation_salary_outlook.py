"""
Populate public.occupation table with salary and outlook data for demo purposes.

This creates entries with reasonable dummy data based on occupation SOC codes.
For production, this would be populated from O*NET or BLS data sources.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import random
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

print(f"Using database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
engine = create_engine(DATABASE_URL)


def generate_salary_for_soc(soc_code: str) -> float:
    """Generate reasonable salary based on SOC major group."""
    # Extract major group from SOC code (first 2 digits)
    major_group = soc_code.split('-')[0]
    
    # Salary ranges by major SOC group (approximate medians)
    salary_ranges = {
        '11': (70000, 130000),   # Management
        '13': (55000, 95000),    # Business/Financial
        '15': (75000, 120000),   # Computer/Math
        '17': (60000, 95000),    # Architecture/Engineering
        '19': (60000, 90000),    # Life/Physical/Social Science
        '21': (45000, 75000),    # Community/Social Service
        '23': (50000, 85000),    # Legal
        '25': (48000, 75000),    # Education
        '27': (45000, 75000),    # Arts/Design/Media
        '29': (60000, 95000),    # Healthcare Practitioners
        '31': (30000, 50000),    # Healthcare Support
        '33': (45000, 75000),    # Protective Service
        '35': (30000, 48000),    # Food Preparation/Service
        '37': (35000, 55000),    # Building Maintenance
        '39': (28000, 45000),    # Personal Care
        '41': (40000, 75000),    # Sales
        '43': (35000, 55000),    # Office/Administrative
        '45': (38000, 58000),    # Farming/Fishing/Forestry
        '47': (40000, 65000),    # Construction/Extraction
        '49': (42000, 65000),    # Installation/Maintenance/Repair
        '51': (38000, 62000),    # Production
        '53': (35000, 55000),    # Transportation
    }
    
    min_sal, max_sal = salary_ranges.get(major_group, (45000, 75000))
    # Add some variation
    return round(random.uniform(min_sal, max_sal), -3)  # Round to nearest 1000


def generate_outlook_for_soc(soc_code: str) -> str:
    """Generate job outlook based on SOC code patterns."""
    major_group = soc_code.split('-')[0]
    
    # Growth outlook by major group (general trends)
    # Based on BLS projections
    high_growth = ['11', '13', '15', '29', '19', '21']  # Management, Business, Tech, Healthcare, Science
    moderate_growth = ['17', '23', '25', '27', '33', '41']  # Engineering, Legal, Education, Arts, Sales
    # Everything else: Average or slower
    
    if major_group in high_growth:
        return random.choice([
            "Much faster than average",
            "Faster than average",
            "Much faster than average"
        ])
    elif major_group in moderate_growth:
        return random.choice([
            "Faster than average",
            "Average",
            "Faster than average"
        ])
    else:
        return random.choice([
            "Average",
            "Slower than average",
            "Average"
        ])


def get_job_zone_from_onet(db: Session, onet_code: str) -> int:
    """Get job zone from O*NET data."""
    query = text("""
        SELECT CAST(job_zone AS INTEGER) as jz
        FROM onet.job_zones
        WHERE onetsoc_code = :code
        LIMIT 1
    """)
    result = db.execute(query, {"code": onet_code}).first()
    return result.jz if result else 3  # Default to 3 if not found


def populate_occupations():
    """Populate public.occupation with salary and outlook data."""
    with Session(engine) as db:
        # Get all O*NET occupation codes
        query = text("""
            SELECT DISTINCT onetsoc_code 
            FROM onet.occupation_data 
            ORDER BY onetsoc_code
        """)
        
        onet_codes = db.execute(query).fetchall()
        
        print(f"Found {len(onet_codes)} occupations to process")
        
        # Check if table exists, create if not
        create_table = text("""
            CREATE TABLE IF NOT EXISTS public.occupation (
                onet_code VARCHAR(10) PRIMARY KEY REFERENCES onet.occupation_data(onetsoc_code),
                median_annual_wage FLOAT,
                employment_outlook VARCHAR(50) NOT NULL,
                job_zone INTEGER NOT NULL,
                interest_codes JSONB DEFAULT '[]',
                interest_scores JSONB DEFAULT '{}',
                onet_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute(create_table)
        db.commit()
        
        inserted = 0
        updated = 0
        
        for row in onet_codes:
            onet_code = row[0]
            
            # Check if already exists
            check_query = text("SELECT onet_code FROM public.occupation WHERE onet_code = :code")
            exists = db.execute(check_query, {"code": onet_code}).first()
            
            salary = generate_salary_for_soc(onet_code)
            outlook = generate_outlook_for_soc(onet_code)
            job_zone = get_job_zone_from_onet(db, onet_code)
            onet_url = f"https://www.onetonline.org/link/summary/{onet_code}"
            
            if exists:
                # Update existing
                update_query = text("""
                    UPDATE public.occupation 
                    SET median_annual_wage = :salary,
                        employment_outlook = :outlook,
                        job_zone = :job_zone,
                        onet_url = :url,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE onet_code = :code
                """)
                db.execute(update_query, {
                    "code": onet_code,
                    "salary": salary,
                    "outlook": outlook,
                    "job_zone": job_zone,
                    "url": onet_url
                })
                updated += 1
            else:
                # Insert new
                insert_query = text("""
                    INSERT INTO public.occupation 
                    (onet_code, median_annual_wage, employment_outlook, job_zone, 
                     interest_codes, interest_scores, top_skills, onet_url, last_updated,
                     created_at, updated_at)
                    VALUES (:code, :salary, :outlook, :job_zone, 
                            '[]'::jsonb, '{}'::jsonb, '[]'::jsonb, :url, CURRENT_TIMESTAMP,
                            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """)
                db.execute(insert_query, {
                    "code": onet_code,
                    "salary": salary,
                    "outlook": outlook,
                    "job_zone": job_zone,
                    "url": onet_url
                })
                inserted += 1
            
            if (inserted + updated) % 100 == 0:
                print(f"Processed {inserted + updated} occupations...")
                db.commit()
        
        db.commit()
        print(f"\nComplete!")
        print(f"Inserted: {inserted}")
        print(f"Updated: {updated}")
        print(f"Total: {inserted + updated}")


if __name__ == "__main__":
    print("Populating occupation salary and outlook data...")
    populate_occupations()
    print("Done!")
