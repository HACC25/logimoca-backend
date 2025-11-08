"""Test cases for the Skill model."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.models import Base, Skill

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

def test_skill_creation(db_session):
    """Test creating a Skill with required fields."""
    skill = Skill(
        onet_element_id="2.B.1",
        name="Critical Thinking",
        category="Complex Problem Solving",
        task_statement="Using logic and reasoning to identify strengths and weaknesses of alternative solutions.",
        anchor_low="Decide what to eat for lunch",
        anchor_high="Evaluate the effectiveness of a new healthcare policy"
    )
    
    db_session.add(skill)
    db_session.commit()
    
    saved_skill = db_session.query(Skill).filter_by(onet_element_id="2.B.1").first()
    assert saved_skill.name == "Critical Thinking"
    assert saved_skill.category == "Complex Problem Solving"
    assert "logic and reasoning" in saved_skill.task_statement
    assert saved_skill.anchor_low == "Decide what to eat for lunch"
    assert saved_skill.anchor_high == "Evaluate the effectiveness of a new healthcare policy"
    assert saved_skill.mean_importance is None
    assert saved_skill.mean_level is None
    assert isinstance(saved_skill.created_at, datetime)
    assert isinstance(saved_skill.updated_at, datetime)

def test_skill_with_statistics(db_session):
    """Test creating a Skill with statistical data."""
    skill = Skill(
        onet_element_id="2.A.1.a",
        name="Reading Comprehension",
        category="Basic Skills",
        task_statement="Understanding written sentences and paragraphs in work related documents.",
        anchor_low="Read step-by-step instructions",
        anchor_high="Read and understand scientific research papers",
        mean_importance=4.2,
        mean_level=3.8
    )
    
    db_session.add(skill)
    db_session.commit()
    
    saved_skill = db_session.query(Skill).filter_by(onet_element_id="2.A.1.a").first()
    assert saved_skill.mean_importance == pytest.approx(4.2)
    assert saved_skill.mean_level == pytest.approx(3.8)

def test_skill_missing_required_field(db_session):
    """Test that creating a Skill without required fields raises an error."""
    skill = Skill(
        onet_element_id="TEST123",
        name="Incomplete Skill"
        # Missing required fields
    )
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an error
        db_session.add(skill)
        db_session.commit()

def test_skill_duplicate_element_id(db_session):
    """Test that creating Skills with duplicate O*NET element IDs raises an error."""
    skill1 = Skill(
        onet_element_id="DUP.1",
        name="First Skill",
        category="Test Category",
        task_statement="First task statement",
        anchor_low="First low anchor",
        anchor_high="First high anchor"
    )
    
    skill2 = Skill(
        onet_element_id="DUP.1",  # Same element ID
        name="Second Skill",
        category="Test Category",
        task_statement="Second task statement",
        anchor_low="Second low anchor",
        anchor_high="Second high anchor"
    )
    
    db_session.add(skill1)
    db_session.commit()
    
    with pytest.raises(Exception):  # SQLAlchemy will raise an IntegrityError
        db_session.add(skill2)
        db_session.commit()

def test_skill_string_representation():
    """Test the string representation of a Skill."""
    skill = Skill(
        onet_element_id="2.B.2",
        name="Complex Problem Solving",
        category="Problem Solving",
        task_statement="Test task statement",
        anchor_low="Test low anchor",
        anchor_high="Test high anchor"
    )
    
    expected = "Skill(onet_element_id='2.B.2', name='Complex Problem Solving', category='Problem Solving')"
    assert str(skill) == expected
    assert repr(skill) == expected