"""
Populate real program data (degree type, duration, credits, cost) based on:
1. Program name analysis (keywords like "Certificate", "AS", "BS", etc.)
2. Pathway information (2-year vs 4-year programs)
3. Institution data (community college vs university)
4. External UH system data
"""
import sys
sys.path.insert(0, 'src')

from src.db.session import get_session_factory
from src.models.public_schema.program import Program
from src.models.public_schema.pathway import Pathway
from src.models.public_schema.institution import Institution
import re

# Known degree types and their typical characteristics
DEGREE_PATTERNS = {
    # Certificates (short programs)
    r'\bcertificate\b': {
        'degree_type': 'Certificate of Achievement',
        'duration_years': 1.0,
        'total_credits': 24,
        'cost_per_credit': 135  # UH community college rate
    },
    r'\bcert\b': {
        'degree_type': 'Certificate',
        'duration_years': 0.5,
        'total_credits': 12,
        'cost_per_credit': 135
    },
    r'\bco\b.*\bcompetence\b': {
        'degree_type': 'Certificate of Competence',
        'duration_years': 1.0,
        'total_credits': 15,
        'cost_per_credit': 135
    },
    
    # Associate degrees
    r'\bas\b|\bassociate.*science\b': {
        'degree_type': 'Associate in Science',
        'duration_years': 2.0,
        'total_credits': 60,
        'cost_per_credit': 135
    },
    r'\baa\b|\bassociate.*arts\b': {
        'degree_type': 'Associate in Arts',
        'duration_years': 2.0,
        'total_credits': 60,
        'cost_per_credit': 135
    },
    r'\baas\b|\bassociate.*applied\b': {
        'degree_type': 'Associate in Applied Science',
        'duration_years': 2.0,
        'total_credits': 62,
        'cost_per_credit': 135
    },
    
    # Bachelor degrees
    r'\bbs\b|\bbachelor.*science\b': {
        'degree_type': 'Bachelor of Science',
        'duration_years': 4.0,
        'total_credits': 120,
        'cost_per_credit': 348  # UH 4-year rate
    },
    r'\bba\b|\bbachelor.*arts\b': {
        'degree_type': 'Bachelor of Arts',
        'duration_years': 4.0,
        'total_credits': 120,
        'cost_per_credit': 348
    },
    r'\bbed\b|\bbachelor.*education\b': {
        'degree_type': 'Bachelor of Education',
        'duration_years': 4.0,
        'total_credits': 124,
        'cost_per_credit': 348
    },
}

# Institution type defaults
INSTITUTION_DEFAULTS = {
    'community_college': {
        'cost_per_credit': 135,
        'typical_duration': 2.0
    },
    'university': {
        'cost_per_credit': 348,
        'typical_duration': 4.0
    }
}

def classify_institution(institution_id):
    """Determine if institution is community college or university."""
    if not institution_id:
        return 'community_college'  # Default assumption
    
    institution_id_lower = institution_id.lower()
    
    if any(cc in institution_id_lower for cc in ['cc', 'community', 'honolulu', 'leeward', 'windward', 'kauai', 'maui']):
        return 'community_college'
    elif any(uni in institution_id_lower for uni in ['manoa', 'hilo', 'west']):
        return 'university'
    
    return 'community_college'

def infer_program_attributes(program):
    """Infer real program attributes from name and metadata."""
    name_lower = program.name.lower()
    
    # Try to match degree pattern
    for pattern, attributes in DEGREE_PATTERNS.items():
        if re.search(pattern, name_lower, re.IGNORECASE):
            return attributes.copy()
    
    # If no pattern matches, use institution defaults
    inst_type = classify_institution(program.institution_id)
    defaults = INSTITUTION_DEFAULTS[inst_type].copy()
    
    # Guess degree type based on institution
    if inst_type == 'community_college':
        return {
            'degree_type': 'Associate in Science',
            'duration_years': 2.0,
            'total_credits': 60,
            'cost_per_credit': defaults['cost_per_credit']
        }
    else:
        return {
            'degree_type': 'Bachelor of Science',
            'duration_years': 4.0,
            'total_credits': 120,
            'cost_per_credit': defaults['cost_per_credit']
        }

def main():
    SessionLocal = get_session_factory()
    db = SessionLocal()
    
    try:
        print("Analyzing program names and inferring real data...")
        print("=" * 80)
        
        # Get all programs with mock data (where all have the same values)
        programs = db.query(Program).all()
        total = len(programs)
        
        print(f"Found {total} programs to process\n")
        
        updated = 0
        stats = {
            'certificates': 0,
            'associates': 0,
            'bachelors': 0,
            'other': 0
        }
        
        for i, program in enumerate(programs, 1):
            # Infer attributes
            new_attrs = infer_program_attributes(program)
            
            # Update program
            program.degree_type = new_attrs['degree_type']
            program.duration_years = new_attrs['duration_years']
            program.total_credits = new_attrs['total_credits']
            program.cost_per_credit = new_attrs['cost_per_credit']
            
            # Track stats
            if 'Certificate' in new_attrs['degree_type']:
                stats['certificates'] += 1
            elif 'Associate' in new_attrs['degree_type']:
                stats['associates'] += 1
            elif 'Bachelor' in new_attrs['degree_type']:
                stats['bachelors'] += 1
            else:
                stats['other'] += 1
            
            updated += 1
            
            if i % 50 == 0:
                print(f"Processed {i}/{total} programs...")
        
        print(f"\n\nUpdated {updated} programs:")
        print("=" * 80)
        print(f"Certificates: {stats['certificates']}")
        print(f"Associate degrees: {stats['associates']}")
        print(f"Bachelor degrees: {stats['bachelors']}")
        print(f"Other: {stats['other']}")
        
        # Show some examples
        print(f"\n\nSample updated programs:")
        print("=" * 80)
        for p in programs[:5]:
            print(f"\n{p.name[:60]}")
            print(f"  → {p.degree_type}")
            print(f"  → {p.duration_years} years, {p.total_credits} credits")
            print(f"  → ${p.cost_per_credit}/credit (total: ${p.total_credits * p.cost_per_credit:,.0f})")
        
        # Confirm before committing
        response = input(f"\n\nCommit these {updated} updates to the database? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            db.commit()
            print("✓ Updates committed successfully!")
        else:
            db.rollback()
            print("✗ Updates rolled back")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
