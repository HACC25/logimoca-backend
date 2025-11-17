from pydantic import BaseModel
from typing import Optional


class ProgramSummary(BaseModel):
    id: str
    name: str
    institution: Optional[str] = None
    degree_type: Optional[str] = None
    duration_years: Optional[float] = None
    cost_total: Optional[float] = None


class ProgramSearchRequest(BaseModel):
    query: str
    top_k: int = 10


class ProgramRecommendation(BaseModel):
    program: ProgramSummary
    score: float
    preview: Optional[str] = None
