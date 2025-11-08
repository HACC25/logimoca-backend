"""Test cases for the Institution model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, Institution

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

def test_institution_creation(db_session):
    """Test creating an Institution with required fields."""
    institution = Institution(
        id="UH_MANOA",
        name="University of Hawaiʻi at Mānoa",
        type="4-year",
        location="Oʻahu",
        website_url="https://manoa.hawaii.edu"
    )
    
    db_session.add(institution)
    db_session.commit()
    
    saved_inst = db_session.query(Institution).filter_by(id="UH_MANOA").first()
    assert saved_inst.name == "University of Hawaiʻi at Mānoa"
    assert saved_inst.type == "4-year"
    assert saved_inst.location == "Oʻahu"
    assert saved_inst.website_url == "https://manoa.hawaii.edu"
    assert saved_inst.campus is None
    assert saved_inst.contact_email is None
    assert saved_inst.latitude is None
    assert saved_inst.longitude is None
    assert isinstance(saved_inst.created_at, datetime)
    assert isinstance(saved_inst.updated_at, datetime)

def test_institution_all_fields(db_session):
    """Test creating an Institution with all fields including optional ones."""
    institution = Institution(
        id="KAP_CC",
        name="Kapiʻolani Community College",
        type="2-year",
        location="Oʻahu",
        campus="Diamond Head Campus",
        website_url="https://kapiolani.hawaii.edu",
        contact_email="kapinfo@hawaii.edu",
        latitude=21.2673,
        longitude=-157.8042
    )
    
    db_session.add(institution)
    db_session.commit()
    
    saved_inst = db_session.query(Institution).filter_by(id="KAP_CC").first()
    assert saved_inst.campus == "Diamond Head Campus"
    assert saved_inst.contact_email == "kapinfo@hawaii.edu"
    assert pytest.approx(saved_inst.latitude) == 21.2673
    assert pytest.approx(saved_inst.longitude) == -157.8042

def test_institution_missing_required_field(db_session):
    """Test that creating an Institution without required fields raises an error."""
    institution = Institution(
        id="TEST",
        name="Test Institution"
        # Missing required type, location, and website_url
    )
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.add(institution)
        db_session.commit()

def test_institution_duplicate_id(db_session):
    """Test that creating Institutions with duplicate IDs raises an error."""
    inst1 = Institution(
        id="DUP",
        name="First Institution",
        type="4-year",
        location="Oʻahu",
        website_url="https://example.com/first"
    )
    
    inst2 = Institution(
        id="DUP",  # Same ID as inst1
        name="Second Institution",
        type="2-year",
        location="Maui",
        website_url="https://example.com/second"
    )
    
    db_session.add(inst1)
    db_session.commit()
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        db_session.add(inst2)
        db_session.commit()

def test_institution_string_representation():
    """Test the string representation of an Institution."""
    institution = Institution(
        id="TEST",
        name="Test Institution",
        type="4-year",
        location="Oʻahu",
        website_url="https://test.hawaii.edu"
    )
    
    expected = "Institution(id='TEST', name='Test Institution', type='4-year')"
    assert str(institution) == expected
    assert repr(institution) == expected