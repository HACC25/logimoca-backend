"""Test cases for the Sector model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, Sector

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

def test_sector_creation(db_session):
    """Test creating a Sector with all required fields."""
    sector = Sector(
        id="AFNRM",
        name="Agriculture, Food & Natural Resource Management",
        description="Programs related to agriculture and natural resources",
        pathway_url="https://example.com/pathways/afnrm"
    )
    
    db_session.add(sector)
    db_session.commit()
    
    saved_sector = db_session.query(Sector).filter_by(id="AFNRM").first()
    assert saved_sector.name == "Agriculture, Food & Natural Resource Management"
    assert saved_sector.description == "Programs related to agriculture and natural resources"
    assert saved_sector.pathway_url == "https://example.com/pathways/afnrm"
    assert saved_sector.icon_url is None
    assert isinstance(saved_sector.created_at, datetime)
    assert isinstance(saved_sector.updated_at, datetime)

def test_sector_with_icon(db_session):
    """Test creating a Sector with an optional icon URL."""
    sector = Sector(
        id="TECH",
        name="Technology",
        description="Technology programs",
        pathway_url="https://example.com/pathways/tech",
        icon_url="https://example.com/icons/tech.png"
    )
    
    db_session.add(sector)
    db_session.commit()
    
    saved_sector = db_session.query(Sector).filter_by(id="TECH").first()
    assert saved_sector.icon_url == "https://example.com/icons/tech.png"

def test_sector_missing_required_field(db_session):
    """Test that creating a Sector without required fields raises an error."""
    sector = Sector(
        id="TEST",
        name="Test Sector"
        # Missing required description and pathway_url
    )
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.add(sector)
        db_session.commit()

def test_sector_duplicate_id(db_session):
    """Test that creating Sectors with duplicate IDs raises an error."""
    sector1 = Sector(
        id="DUP",
        name="First Sector",
        description="First description",
        pathway_url="https://example.com/first"
    )
    
    sector2 = Sector(
        id="DUP",  # Same ID as sector1
        name="Second Sector",
        description="Second description",
        pathway_url="https://example.com/second"
    )
    
    db_session.add(sector1)
    db_session.commit()
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        db_session.add(sector2)
        db_session.commit()

def test_sector_string_representation():
    """Test the string representation of a Sector."""
    sector = Sector(
        id="TEST",
        name="Test Sector",
        description="Test description",
        pathway_url="https://example.com/test"
    )
    
    assert str(sector) == "Sector(id='TEST', name='Test Sector')"
    assert repr(sector) == "Sector(id='TEST', name='Test Sector')"