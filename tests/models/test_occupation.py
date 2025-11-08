"""Test cases for the Occupation model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, Occupation

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

def test_occupation_creation(db_session):
    """Test creating an Occupation with required fields."""
    occupation = Occupation(
        onet_code="15-1251.00",
        title="Computer Programmer",
        description="Write, update, and maintain computer programs",
        employment_outlook="Stable",
        job_zone=4,
        typical_education="Bachelor's degree",
        onet_url="https://www.onetonline.org/link/summary/15-1251.00"
    )
    
    db_session.add(occupation)
    db_session.commit()
    
    saved_occ = db_session.query(Occupation).filter_by(onet_code="15-1251.00").first()
    assert saved_occ.title == "Computer Programmer"
    assert saved_occ.description == "Write, update, and maintain computer programs"
    assert saved_occ.employment_outlook == "Stable"
    assert saved_occ.job_zone == 4
    assert saved_occ.typical_education == "Bachelor's degree"
    assert saved_occ.median_annual_wage is None
    assert saved_occ.interest_codes == []
    assert saved_occ.interest_scores == {}
    assert saved_occ.top_skills == []
    assert isinstance(saved_occ.created_at, datetime)
    assert isinstance(saved_occ.updated_at, datetime)
    assert isinstance(saved_occ.last_updated, datetime)

def test_occupation_all_fields(db_session):
    """Test creating an Occupation with all fields including optional ones."""
    occupation = Occupation(
        onet_code="11-1021.00",
        title="General Manager",
        description="Plan and direct organizational operations",
        employment_outlook="Growing",
        job_zone=4,
        typical_education="Bachelor's degree",
        onet_url="https://www.onetonline.org/link/summary/11-1021.00",
        median_annual_wage=120000.0,
        interest_codes=["E", "S", "C"],
        interest_scores={"E": 95, "S": 85, "C": 75},
        top_skills=[
            {"id": "2.B.1", "name": "Critical Thinking", "score": 78},
            {"id": "2.B.4", "name": "Management of Personnel", "score": 75}
        ]
    )
    
    db_session.add(occupation)
    db_session.commit()
    
    saved_occ = db_session.query(Occupation).filter_by(onet_code="11-1021.00").first()
    assert saved_occ.median_annual_wage == 120000.0
    assert saved_occ.interest_codes == ["E", "S", "C"]
    assert saved_occ.interest_scores["E"] == 95
    assert len(saved_occ.top_skills) == 2
    assert saved_occ.top_skills[0]["name"] == "Critical Thinking"

def test_occupation_json_field_defaults(db_session):
    """Test that JSON fields have correct default values."""
    occupation = Occupation(
        onet_code="TEST123",
        title="Test Occupation",
        description="Testing JSON defaults",
        employment_outlook="Stable",
        job_zone=3,
        typical_education="Associate's degree",
        onet_url="https://example.com/test123"
    )
    
    db_session.add(occupation)
    db_session.commit()
    
    saved_occ = db_session.query(Occupation).filter_by(onet_code="TEST123").first()
    assert isinstance(saved_occ.interest_codes, list)
    assert len(saved_occ.interest_codes) == 0
    assert isinstance(saved_occ.interest_scores, dict)
    assert len(saved_occ.interest_scores) == 0
    assert isinstance(saved_occ.top_skills, list)
    assert len(saved_occ.top_skills) == 0

def test_occupation_missing_required_field(db_session):
    """Test that creating an Occupation without required fields raises an error."""
    occupation = Occupation(
        onet_code="TEST456",
        title="Incomplete Occupation"
        # Missing required fields
    )
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.add(occupation)
        db_session.commit()

def test_occupation_duplicate_onet_code(db_session):
    """Test that creating Occupations with duplicate O*NET codes raises an error."""
    occ1 = Occupation(
        onet_code="DUP-000",
        title="First Occupation",
        description="First description",
        employment_outlook="Stable",
        job_zone=3,
        typical_education="Bachelor's degree",
        onet_url="https://example.com/dup000"
    )
    
    occ2 = Occupation(
        onet_code="DUP-000",  # Same O*NET code
        title="Second Occupation",
        description="Second description",
        employment_outlook="Growing",
        job_zone=4,
        typical_education="Master's degree",
        onet_url="https://example.com/dup000-2"
    )
    
    db_session.add(occ1)
    db_session.commit()
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        db_session.add(occ2)
        db_session.commit()

def test_occupation_string_representation():
    """Test the string representation of an Occupation."""
    occupation = Occupation(
        onet_code="15-1133.00",
        title="Software Developer",
        description="Develop software applications",
        employment_outlook="Growing",
        job_zone=4,
        typical_education="Bachelor's degree",
        onet_url="https://example.com/15-1133.00"
    )
    
    expected = "Occupation(onet_code='15-1133.00', title='Software Developer', job_zone=4)"
    assert str(occupation) == expected
    assert repr(occupation) == expected