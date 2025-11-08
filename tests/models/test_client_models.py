"""Test client-side Pydantic models."""

from datetime import datetime
import pytest
from pydantic import ValidationError

from api.models.client_models import (
    ClientModel,
    InterestAssessment,
    SkillsAssessment
)

def test_base_client_model_valid():
    """Test creating a valid base client model."""
    now = datetime.utcnow()
    model = ClientModel(
        session_id="test-session-123",
        created_at=now,
        completion_time_seconds=300
    )
    assert model.session_id == "test-session-123"
    assert model.created_at == now
    assert model.completion_time_seconds == 300

def test_base_client_model_invalid():
    """Test validation errors in base client model."""
    with pytest.raises(ValidationError) as exc_info:
        ClientModel(
            session_id="short",  # Too short
            completion_time_seconds=-1  # Invalid
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 2
    error_fields = [e["loc"][0] for e in errors]
    assert "session_id" in error_fields
    assert "completion_time_seconds" in error_fields

def test_interest_assessment_valid():
    """Test creating a valid interest assessment."""
    assessment = InterestAssessment(
        session_id="test-session-123",
        responses={"Q1": "A", "Q2": "B"},
        riasec_scores={"R": 80.5, "I": 65.0, "A": 45.5},
        riasec_code="RIA",
        completion_time_seconds=600
    )
    assert assessment.session_id == "test-session-123"
    assert assessment.responses == {"Q1": "A", "Q2": "B"}
    assert assessment.riasec_scores == {"R": 80.5, "I": 65.0, "A": 45.5}
    assert assessment.riasec_code == "RIA"
    assert assessment.completion_time_seconds == 600

def test_interest_assessment_invalid_riasec():
    """Test RIASEC validation."""
    with pytest.raises(ValidationError) as exc_info:
        InterestAssessment(
            session_id="test-session-123",
            responses={"Q1": "A"},
            riasec_scores={"X": 80.5},  # Invalid dimension
            riasec_code="ABC",  # Invalid code
            completion_time_seconds=300
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 2
    error_fields = [e["loc"][0] for e in errors]
    assert "riasec_code" in error_fields
    assert "riasec_scores" in error_fields

def test_interest_assessment_invalid_scores():
    """Test RIASEC score validation."""
    with pytest.raises(ValidationError) as exc_info:
        InterestAssessment(
            session_id="test-session-123",
            responses={"Q1": "A"},
            riasec_scores={"R": 150.0},  # Over 100
            riasec_code="RIA",
            completion_time_seconds=300
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert "riasec_scores" in [e["loc"][0] for e in errors]

def test_skills_assessment_valid():
    """Test creating a valid skills assessment."""
    assessment = SkillsAssessment(
        session_id="test-session-123",
        occupation_pool=["12345678"],
        filtered_skill_ids=["SK123", "SK456"],
        panel_initial_scores={"SK123": 3, "SK456": 4},
        narrative_evidence="I have experience in...",
        refinement_ratings={"SK123": 4, "SK456": 5},
        final_api_string="skill1,skill2",
        llm_justification="Based on evidence...",
        completion_time_seconds=900
    )
    assert assessment.session_id == "test-session-123"
    assert len(assessment.occupation_pool) == 1
    assert len(assessment.filtered_skill_ids) == 2
    assert assessment.panel_initial_scores == {"SK123": 3, "SK456": 4}
    assert assessment.completion_time_seconds == 900

def test_skills_assessment_invalid_ratings():
    """Test skills ratings validation."""
    with pytest.raises(ValidationError) as exc_info:
        SkillsAssessment(
            session_id="test-session-123",
            occupation_pool=["12345678"],
            filtered_skill_ids=["SK123"],
            panel_initial_scores={"SK123": 6},  # Over 5
            narrative_evidence="Test",
            refinement_ratings={"SK123": 3},
            final_api_string="test",
            llm_justification="test",
            completion_time_seconds=300
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert "panel_initial_scores" in [e["loc"][0] for e in errors]

def test_skills_assessment_invalid_onet():
    """Test O*NET code validation."""
    with pytest.raises(ValidationError) as exc_info:
        SkillsAssessment(
            session_id="test-session-123",
            occupation_pool=["123"],  # Invalid format
            filtered_skill_ids=["SK123"],
            panel_initial_scores={"SK123": 3},
            narrative_evidence="Test",
            refinement_ratings={"SK123": 3},
            final_api_string="test",
            llm_justification="test",
            completion_time_seconds=300
        )
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert "occupation_pool" in [e["loc"][0] for e in errors]