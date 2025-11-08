"""Test cases for association tables."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import (
    Base, Skill, Occupation, Program, Sector, Institution,
    occupation_skill, program_occupation
)

# Setup test database
@pytest.fixture(scope="function")
def engine():
    """Create a fresh database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(engine):
    """Create a new database session for a test."""
    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture
def sample_skill(db_session):
    """Create a sample skill for testing."""
    skill = Skill(
        onet_element_id="2.B.1",
        name="Critical Thinking",
        category="Complex Problem Solving",
        task_statement="Using logic to solve problems",
        anchor_low="Basic problem solving",
        anchor_high="Complex problem solving"
    )
    db_session.add(skill)
    db_session.commit()
    return skill

@pytest.fixture
def sample_occupation(db_session):
    """Create a sample occupation for testing."""
    occupation = Occupation(
        onet_code="15-1256.00",
        title="Software Developer",
        description="Develop software applications",
        employment_outlook="Growing",
        job_zone=4,
        typical_education="Bachelor's degree",
        onet_url="https://www.onetonline.org/link/summary/15-1256.00"
    )
    db_session.add(occupation)
    db_session.commit()
    return occupation

@pytest.fixture
def sample_program(db_session):
    """Create a sample program with required relationships."""
    sector = Sector(
        id="TECH",
        name="Technology",
        description="Technology sector",
        pathway_url="https://example.com/tech"
    )
    
    institution = Institution(
        id="TEST_INST",
        name="Test Institution",
        type="4-year",
        location="Oʻahu",
        website_url="https://example.edu"
    )
    
    program = Program(
        id="TEST_PROG",
        sector=sector,
        institution=institution,
        name="Computer Science",
        degree_type="Bachelor",
        duration_years=4.0,
        total_credits=120,
        cost_per_credit=300.0,
        description="CS program",
        program_url="https://example.edu/cs"
    )
    
    db_session.add_all([sector, institution, program])
    db_session.commit()
    return program

def test_occupation_skill_association(db_session, sample_occupation, sample_skill):
    """Test creating an occupation-skill association."""
    # Create association via SQL
    db_session.execute(
        occupation_skill.insert().values(
            occupation_onet_code=sample_occupation.onet_code,
            skill_onet_element_id=sample_skill.onet_element_id,
            importance=4.5,
            level=5.0
        )
    )
    db_session.commit()
    
    # Verify relationship through ORM
    assert len(sample_occupation.skills) == 1
    assert sample_occupation.skills[0].onet_element_id == sample_skill.onet_element_id
    assert len(sample_skill.occupations) == 1
    assert sample_skill.occupations[0].onet_code == sample_occupation.onet_code
    
    # Verify association data
    result = db_session.execute(
        occupation_skill.select().where(
            occupation_skill.c.occupation_onet_code == sample_occupation.onet_code
        )
    ).first()
    assert result.importance == 4.5
    assert result.level == 5.0

def test_program_occupation_association(db_session, sample_program, sample_occupation):
    """Test creating a program-occupation association."""
    # Create association via SQL
    db_session.execute(
        program_occupation.insert().values(
            program_id=sample_program.id,
            occupation_onet_code=sample_occupation.onet_code,
            confidence=0.85
        )
    )
    db_session.commit()
    
    # Verify relationship through ORM
    assert len(sample_program.occupations) == 1
    assert sample_program.occupations[0].onet_code == sample_occupation.onet_code
    assert len(sample_occupation.programs) == 1
    assert sample_occupation.programs[0].id == sample_program.id
    
    # Verify association data
    result = db_session.execute(
        program_occupation.select().where(
            program_occupation.c.program_id == sample_program.id
        )
    ).first()
    assert result.confidence == 0.85
    assert isinstance(result.created_at, datetime)

def test_cascade_delete_occupation(db_session, sample_occupation, sample_skill):
    """Test that deleting an occupation cascades to associations."""
    # Create association
    db_session.execute(
        occupation_skill.insert().values(
            occupation_onet_code=sample_occupation.onet_code,
            skill_onet_element_id=sample_skill.onet_element_id,
            importance=4.0,
            level=3.0
        )
    )
    db_session.commit()
    
    # Delete occupation
    db_session.delete(sample_occupation)
    db_session.commit()
    
    # Verify association is deleted
    result = db_session.execute(
        occupation_skill.select().where(
            occupation_skill.c.skill_onet_element_id == sample_skill.onet_element_id
        )
    ).first()
    assert result is None

def test_cascade_delete_program(db_session, sample_program, sample_occupation):
    """Test that deleting a program cascades to associations."""
    # Create association
    db_session.execute(
        program_occupation.insert().values(
            program_id=sample_program.id,
            occupation_onet_code=sample_occupation.onet_code,
            confidence=0.9
        )
    )
    db_session.commit()
    
    # Delete program
    db_session.delete(sample_program)
    db_session.commit()
    
    # Verify association is deleted
    result = db_session.execute(
        program_occupation.select().where(
            program_occupation.c.occupation_onet_code == sample_occupation.onet_code
        )
    ).first()
    assert result is None