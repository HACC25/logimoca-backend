from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.api.v1.schemas.assessment import (
    RiasecCodeRequest,
    RiasecResult,
    SkillRatingsSubmission,
    SkillWeightsResponse,
    InterestQuizRequest,
    InterestQuizResponse,
    SkillTriageResponse,
)
from src.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.post("/riasec", response_model=RiasecResult)
def submit_riasec_code(
    payload: RiasecCodeRequest,
    db: Session = Depends(get_db),
    service: AssessmentService = Depends(AssessmentService),
):
    """Submit 3-letter RIASEC code and receive matched occupations + baseline skill panel."""
    return service.process_riasec_code(payload, db)


@router.post("/skills/weights", response_model=SkillWeightsResponse)
def compute_skill_weights(
    submission: SkillRatingsSubmission,
    service: AssessmentService = Depends(AssessmentService),
):
    """Compute adjusted skill weights from user ratings and static 40-skill distributions."""
    return service.compute_skill_weights(submission)



# Legacy placeholder endpoints kept for backward compatibility (can be removed later)
@router.post("/interest", response_model=InterestQuizResponse)
def submit_interest_quiz(
    payload: InterestQuizRequest,
    service: AssessmentService = Depends(AssessmentService),
):
    return service.process_interest_quiz(payload)

@router.post("/skills/triage", response_model=SkillTriageResponse)
def triage_skills(
    service: AssessmentService = Depends(AssessmentService),
):
    return service.triage_skills()