from pydantic import BaseModel
from typing import List, Optional


class OccupationSummary(BaseModel):
    onet_code: str
    title: str
    match_score: Optional[float] = None
    median_wage: Optional[float] = None
    outlook: Optional[str] = None
    top_skills: List[str] = []
