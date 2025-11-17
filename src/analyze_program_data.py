"""
Analyze program data quality and identify fields needing enrichment.
"""
import sys
sys.path.insert(0, 'src')

from db.session import get_session_factory
from models.public_schema.program import Program
from sqlalchemy import func

def main():
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        # Get sample programs
        programs = db.query(Program).limit(3).all()
        
        print('Sample Programs:')
        print('=' * 80)
        for p in programs:
            print(f'\nID: {p.id}')
            print(f'  Name: {p.name[:60]}...' if len(p.name) > 60 else f'  Name: {p.name}')
            print(f'  Degree: {p.degree_type}')
            print(f'  Duration: {p.duration_years} years, Credits: {p.total_credits}')
            desc_preview = (p.description[:60] + '...') if p.description and len(p.description) > 60 else (p.description or 'None')
            print(f'  Description: {desc_preview}')
        
        # Get stats on missing data
        total = db.query(func.count(Program.id)).scalar()
        missing_desc = db.query(func.count(Program.id)).filter(Program.description == None).scalar()
        missing_prereq = db.query(func.count(Program.id)).filter(Program.prerequisites == None).scalar()
        missing_url = db.query(func.count(Program.id)).filter(Program.program_url == None).scalar()
        missing_delivery = db.query(func.count(Program.id)).filter(Program.delivery_modes == None).scalar()
        missing_cost = db.query(func.count(Program.id)).filter(Program.cost_per_credit == None).scalar()
        
        print(f'\n\nData Completeness:')
        print('=' * 80)
        print(f'Total programs: {total}')
        print(f'Missing descriptions: {missing_desc} ({missing_desc/total*100:.1f}%)')
        print(f'Missing prerequisites: {missing_prereq} ({missing_prereq/total*100:.1f}%)')
        print(f'Missing URLs: {missing_url} ({missing_url/total*100:.1f}%)')
        print(f'Missing delivery modes: {missing_delivery} ({missing_delivery/total*100:.1f}%)')
        print(f'Missing cost per credit: {missing_cost} ({missing_cost/total*100:.1f}%)')
        
        # Check for duplicates or similar programs
        print(f'\n\nChecking for potential duplicates:')
        print('=' * 80)
        
        # Get programs grouped by name
        from sqlalchemy import distinct
        program_names = db.query(Program.name, func.count(Program.id).label('count')).group_by(Program.name).having(func.count(Program.id) > 1).all()
        
        if program_names:
            print(f'Found {len(program_names)} program names with duplicates:')
            for name, count in program_names[:5]:
                name_short = (name[:60] + '...') if len(name) > 60 else name
                print(f'  "{name_short}" appears {count} times')
        else:
            print('No exact duplicate program names found.')
            
    finally:
        db.close()

if __name__ == "__main__":
    main()
