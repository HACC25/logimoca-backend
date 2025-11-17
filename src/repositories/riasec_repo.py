"""Repository for RIASEC profile lookups and matched jobs retrieval."""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from models.riasec_profile import RiasecProfile
from models.interest_matched_job import InterestMatchedJob


class RiasecRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, code: str) -> Optional[RiasecProfile]:
        return (
            self.db.query(RiasecProfile)
            .filter(RiasecProfile.code == code)
            .options(joinedload(RiasecProfile.matched_jobs))
            .first()
        )

    def get_or_permutation(self, code: str) -> Optional[RiasecProfile]:
        profile = self.get_profile(code)
        if profile:
            return profile
        # Fallback: try sorted permutation if exact code absent
        sorted_code = "".join(sorted(code))
        if sorted_code != code:
            return self.get_profile(sorted_code)
        return None

    def top_matched_jobs(self, profile: RiasecProfile, limit: int = 15) -> List[InterestMatchedJob]:
        # matched_jobs already loaded (joinedload). They may be unsorted; basic sort by interest_sum desc
        jobs = sorted(profile.matched_jobs, key=lambda j: float(j.interest_sum), reverse=True)
        return jobs[:limit]
