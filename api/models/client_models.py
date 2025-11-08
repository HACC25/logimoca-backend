"""Client-side models for request/response validation."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class ClientModel(BaseModel):
    """Base class for client-side models."""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completion_time_seconds: int = Field(..., description="Time taken to complete assessment")

    @field_validator("session_id")
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID format."""
        if not v or len(v) < 8:
            raise ValueError("Session ID must be at least 8 characters")
        return v

    @field_validator("completion_time_seconds")
    def validate_completion_time(cls, v: int) -> int:
        """Validate completion time."""
        if v <= 0:
            raise ValueError("Completion time must be positive")
        return v

class InterestAssessment(ClientModel):
    """RIASEC interest assessment results."""
    responses: Dict[str, str] = Field(..., description="Raw RIASEC question responses")
    riasec_scores: Dict[str, float] = Field(
        default_factory=dict, 
        description="Computed scores for each RIASEC dimension"
    )
    riasec_code: str = Field(..., description="Three-letter RIASEC code")

    @field_validator("riasec_code")
    def validate_riasec_code(cls, v: str) -> str:
        """Validate RIASEC code format."""
        if not v or len(v) != 3 or not v.isalpha() or not v.isupper():
            raise ValueError("RIASEC code must be 3 uppercase letters")
        for letter in v:
            if letter not in "RIASEC":
                raise ValueError("RIASEC code must only contain letters R,I,A,S,E,C")
        return v

    @field_validator("riasec_scores")
    def validate_riasec_scores(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate RIASEC scores."""
        if not v:
            return v
        valid_dims = set("RIASEC")
        for dim, score in v.items():
            if dim not in valid_dims:
                raise ValueError(f"Invalid RIASEC dimension: {dim}")
            if not 0 <= score <= 100:
                raise ValueError(f"Score must be between 0-100: {score}")
        return v

class SkillsAssessment(ClientModel):
    """User skill and aptitude profile for CareerOneStop API."""
    # Phase 1: Filtered occupation data
    occupation_pool: List[str] = Field(..., description="O*NET codes for relevant occupations")
    filtered_skill_ids: List[str] = Field(..., description="O*NET element IDs for relevant skills")
    
    # Phase 2: User input 
    panel_initial_scores: Dict[str, int] = Field(
        ..., description="Initial self-rated scores per skill"
    )
    narrative_evidence: str = Field(..., description="User's evidence narrative")
    refinement_ratings: Dict[str, int] = Field(
        ..., description="Refined ratings after LLM feedback"
    )
    
    # Phase 3: Final output
    final_api_string: str = Field(..., description="API-ready skills string")
    llm_justification: str = Field(..., description="LLM's skills analysis")
    
    @field_validator("panel_initial_scores", "refinement_ratings")
    def validate_ratings(cls, v: Dict[str, int]) -> Dict[str, int]:
        """Validate skill ratings."""
        for skill_id, rating in v.items():
            if not 0 <= rating <= 5:
                raise ValueError(f"Rating must be between 0-5: {rating}")
        return v

    @field_validator("occupation_pool")
    def validate_onet_codes(cls, v: List[str]) -> List[str]:
        """Validate O*NET codes."""
        for code in v:
            if not code.isalnum() or len(code) != 8:
                raise ValueError(f"Invalid O*NET code format: {code}")
        return v