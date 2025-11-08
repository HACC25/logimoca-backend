"""Test cases for the Program model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, Program, Sector, Institution

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
def sample_sector(db_session):
    """Create a sample sector for testing."""
    sector = Sector(
        id="TECH",
        name="Technology",
        description="Technology programs",
        pathway_url="https://example.com/pathways/tech"
    )
    db_session.add(sector)
    db_session.commit()
    return sector

@pytest.fixture
def sample_institution(db_session):
    """Create a sample institution for testing."""
    institution = Institution(
        id="INST_TEST",
        name="Test Institution",
        type="4-year",
        location="Oʻahu",
        website_url="https://example.edu"
    )
    db_session.add(institution)
    db_session.commit()
    return institution

def test_program_creation(db_session, sample_sector, sample_institution):
    """Test creating a Program with required fields."""
    program = Program(
        id="TEST_PROG",
        sector_id=sample_sector.id,
        institution_id=sample_institution.id,
        name="Test Program",
        degree_type="Bachelor",
        duration_years=4.0,
        total_credits=120,
        cost_per_credit=300.0,
        description="A test program description",
        program_url="https://example.edu/program"
    )
    
    db_session.add(program)
    db_session.commit()
    
    saved_prog = db_session.query(Program).filter_by(id="TEST_PROG").first()
    assert saved_prog.name == "Test Program"
    assert saved_prog.degree_type == "Bachelor"
    assert saved_prog.duration_years == 4.0
    assert saved_prog.total_credits == 120
    assert saved_prog.cost_per_credit == 300.0
    assert saved_prog.description == "A test program description"
    assert saved_prog.program_url == "https://example.edu/program"
    assert saved_prog.prerequisites == []  # Default empty list
    assert saved_prog.delivery_modes == []  # Default empty list
    assert isinstance(saved_prog.created_at, datetime)
    assert isinstance(saved_prog.updated_at, datetime)

def test_program_relationships(db_session, sample_sector, sample_institution):
    """Test Program relationships with Sector and Institution."""
    program = Program(
        id="REL_TEST",
        sector_id=sample_sector.id,
        institution_id=sample_institution.id,
        name="Relationship Test Program",
        degree_type="Associate",
        duration_years=2.0,
        total_credits=60,
        cost_per_credit=131.0,
        description="Testing relationships",
        program_url="https://example.edu/rel_test"
    )
    
    db_session.add(program)
    db_session.commit()
    
    # Test bidirectional relationships
    assert program.sector.id == sample_sector.id
    assert program.institution.id == sample_institution.id
    assert program in sample_sector.programs
    assert program in sample_institution.programs

def test_program_with_json_fields(db_session, sample_sector, sample_institution):
    """Test Program with JSON fields populated."""
    program = Program(
        id="JSON_TEST",
        sector_id=sample_sector.id,
        institution_id=sample_institution.id,
        name="JSON Fields Test Program",
        degree_type="Certificate",
        duration_years=1.0,
        total_credits=30,
        cost_per_credit=131.0,
        description="Testing JSON fields",
        program_url="https://example.edu/json_test",
        prerequisites=["MATH 100", "ENG 100"],
        delivery_modes=["In-Person", "Hybrid"]
    )
    
    db_session.add(program)
    db_session.commit()
    
    saved_prog = db_session.query(Program).filter_by(id="JSON_TEST").first()
    assert "MATH 100" in saved_prog.prerequisites
    assert "Hybrid" in saved_prog.delivery_modes

def test_program_missing_required_field(db_session, sample_sector, sample_institution):
    """Test that creating a Program without required fields raises an error."""
    program = Program(
        id="MISSING_TEST",
        sector_id=sample_sector.id,
        institution_id=sample_institution.id,
        name="Incomplete Program"
        # Missing other required fields
    )
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.add(program)
        db_session.commit()

def test_program_invalid_foreign_key(db_session):
    """Test that creating a Program with invalid foreign keys raises an error."""
    with pytest.raises(ValueError, match="Sector ID must be a string"):
        Program(
            id="FK_TEST",
            sector_id=123,  # Wrong type
            institution_id="FAKE_INST",
            name="Foreign Key Test",
            degree_type="Bachelor",
            duration_years=4.0,
            total_credits=120,
            cost_per_credit=300.0,
            description="Testing foreign key constraints",
            program_url="https://example.edu/fk_test"
        )
    
    with pytest.raises(ValueError, match="Institution ID must be a string"):
        Program(
            id="FK_TEST",
            sector_id="TECH",
            institution_id=123,  # Wrong type
            name="Foreign Key Test",
            degree_type="Bachelor",
            duration_years=4.0,
            total_credits=120,
            cost_per_credit=300.0,
            description="Testing foreign key constraints",
            program_url="https://example.edu/fk_test"
        )

def test_program_string_representation(sample_sector, sample_institution):
    """Test the string representation of a Program."""
    program = Program(
        id="REPR_TEST",
        sector_id=sample_sector.id,
        institution_id=sample_institution.id,
        name="String Representation Test",
        degree_type="Master",
        duration_years=2.0,
        total_credits=60,
        cost_per_credit=500.0,
        description="Testing string representation",
        program_url="https://example.edu/repr_test"
    )
    
    expected = "Program(id='REPR_TEST', name='String Representation Test', degree_type='Master')"
    assert str(program) == expected
    assert repr(program) == expected