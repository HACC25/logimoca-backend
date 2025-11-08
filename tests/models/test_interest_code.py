"""Test cases for the InterestCode model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, InterestCode

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

def test_interest_code_creation(db_session):
    """Test creating an InterestCode with required fields."""
    interest = InterestCode(
        code="I",
        name="Investigative",
        description="People with investigative interests like to solve complex problems and conduct research.",
        color_hex="#10B981",
        job_tasks="Conducting experiments, analyzing data, solving mathematical problems",
        work_values="Scientific inquiry, intellectual stimulation, independence"
    )
    
    db_session.add(interest)
    db_session.commit()
    
    saved_interest = db_session.query(InterestCode).filter_by(code="I").first()
    assert saved_interest.name == "Investigative"
    assert "solve complex problems" in saved_interest.description
    assert saved_interest.color_hex == "#10B981"
    assert "experiments" in saved_interest.job_tasks
    assert "Scientific inquiry" in saved_interest.work_values
    assert isinstance(saved_interest.created_at, datetime)
    assert isinstance(saved_interest.updated_at, datetime)

def test_interest_code_invalid_code(db_session):
    """Test that creating an InterestCode with invalid code raises an error."""
    with pytest.raises(ValueError, match="Code must be one of R,I,A,S,E,C"):
        InterestCode(
            code="X",  # Invalid RIASEC code
            name="Invalid",
            description="Test description",
            color_hex="#000000",
            job_tasks="Test tasks",
            work_values="Test values"
        )

def test_interest_code_invalid_color(db_session):
    """Test that creating an InterestCode with invalid color hex raises an error."""
    with pytest.raises(ValueError) as exc_info:
        InterestCode(
            code="R",
            name="Realistic",
            description="Test description",
            color_hex="invalid",  # Not a valid hex color
            job_tasks="Test tasks",
            work_values="Test values"
        )
    assert str(exc_info.value) == "Color must be a valid hex code (e.g., #FF0000)"

def test_interest_code_duplicate_code(db_session):
    """Test that creating InterestCodes with duplicate codes raises an error."""
    interest1 = InterestCode(
        code="S",
        name="Social",
        description="First description",
        color_hex="#F59E0B",
        job_tasks="First tasks",
        work_values="First values"
    )
    
    interest2 = InterestCode(
        code="S",  # Same code as interest1
        name="Different Social",
        description="Second description",
        color_hex="#F59E0B",
        job_tasks="Second tasks",
        work_values="Second values"
    )
    
    db_session.add(interest1)
    db_session.commit()
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        db_session.add(interest2)
        db_session.commit()

def test_interest_code_string_representation():
    """Test the string representation of an InterestCode."""
    interest = InterestCode(
        code="A",
        name="Artistic",
        description="Test description",
        color_hex="#8B5CF6",
        job_tasks="Test tasks",
        work_values="Test values"
    )
    
    expected = "InterestCode(code='A', name='Artistic')"
    assert str(interest) == expected
    assert repr(interest) == expected