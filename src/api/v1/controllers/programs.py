from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.api.v1.schemas.program import ProgramSearchRequest, ProgramRecommendation, ProgramSummary
from src.services.program_search import search_programs, hydrate_programs

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("/")
async def list_programs():
    """Placeholder: return a paginated list of programs."""
    return {"items": [], "total": 0}


@router.post("/recommend", response_model=List[ProgramRecommendation])
def recommend_programs(payload: ProgramSearchRequest, db: Session = Depends(get_db)):
    """Return top-k program recommendations using semantic search over vector_chunks."""
    scored = search_programs(db, query=payload.query, top_k=payload.top_k)
    results = hydrate_programs(db, scored)
    # Coerce into response models
    recs: List[ProgramRecommendation] = []
    for r in results:
        ps = ProgramSummary(**r["program"])  # type: ignore[arg-type]
        recs.append(ProgramRecommendation(program=ps, score=r["score"], preview=r.get("preview")))
    return recs
