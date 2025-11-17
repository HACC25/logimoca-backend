from typing import Dict, List
from pydantic import Field, field_validator

from .client_model import ClientModel


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