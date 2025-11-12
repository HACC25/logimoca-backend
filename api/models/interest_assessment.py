from typing import Dict
from pydantic import Field, field_validator
from .client_model import ClientModel

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