"""Repository for RIASEC profile lookups and matched jobs retrieval."""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import text


class RiasecRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, code: str) -> Optional[Dict]:
        """Get RIASEC profile by code using raw SQL to avoid relationship issues."""
        query = text("SELECT code FROM riasec.riasec_profiles WHERE UPPER(code) = UPPER(:code)")
        result = self.db.execute(query, {"code": code}).first()
        
        if result:
            # Return as dict to avoid ORM relationship issues
            return {"code": result.code}
        return None

    def top_matched_jobs(self, profile: Dict, limit: int = 15) -> List[dict]:
        """Return matched jobs with real titles from onet.occupation_data.
        
        Uses raw SQL to join interest_matched_jobs with onet occupation_data.
        Handles case-insensitive matching for RIASEC codes.
        """
        query = text("""
            SELECT imj.occ_code, od.title
            FROM riasec.interest_matched_jobs imj
            JOIN onet.occupation_data od ON imj.occ_code = od.onetsoc_code
            WHERE UPPER(imj.fk_riasec_code) = UPPER(:code)
            ORDER BY imj.interest_sum DESC
            LIMIT :limit
        """)
        
        results = self.db.execute(query, {"code": profile["code"], "limit": limit}).all()
        return [
            {"occ_code": row.occ_code, "title": row.title}
            for row in results
        ]
