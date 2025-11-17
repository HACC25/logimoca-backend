from typing import Dict, List, Iterable
import json
from pathlib import Path

from api.v1.schemas.assessment import (
    RiasecCodeRequest,
    RiasecResult,
    SkillDefinition,
    SkillRatingsSubmission,
    SkillWeightsResponse,
    SkillWeighted,
    InterestQuizRequest,
    InterestQuizResponse,
    SkillTriageResponse,
)
from repositories.assessment_repo import AssessmentRepository
from repositories.riasec_repo import RiasecRepository
from .static_references.riasec_combo_map import canonical_riasec
from sqlalchemy.orm import Session

STATIC_DIR = Path(__file__).parent / "static_references"
SKILLS_FILE = STATIC_DIR / "oneStop40Skills.json"


class AssessmentService:
    """Service layer for RIASEC interest and skill weighting workflows."""

    def __init__(self) -> None:
        self._skills_cache: List[SkillDefinition] | None = None

    # ---------------- Utility -----------------
    def _load_skill_definitions(self) -> List[SkillDefinition]:
        if self._skills_cache is not None:
            return self._skills_cache
        raw = json.loads(SKILLS_FILE.read_text())
        defs: List[SkillDefinition] = []
        for row in raw:
            defs.append(
                SkillDefinition(
                    element_id=row["ElementId"],
                    name=row["ElementName"],
                    question=row.get("Question", ""),
                    easy_read_description=row.get("EasyReadDescription", ""),
                    anchor_first=row.get("AnchorFirst", ""),
                    anchor_third=row.get("AnchorThrid", ""),
                    anchor_last=row.get("AnchorLast", ""),
                    data_point_20=row.get("DataPoint20", 0.0),
                    data_point_35=row.get("DataPoint35", 0.0),
                    data_point_50=row.get("DataPoint50", 0.0),
                    data_point_65=row.get("DataPoint65", 0.0),
                    data_point_80=row.get("DataPoint80", 0.0),
                )
            )
        self._skills_cache = defs
        return defs

    # ---------------- Interest (RIASEC) -----------------
    def process_riasec_code(self, payload: RiasecCodeRequest, db: Session) -> RiasecResult:
        """Return interest-filtered occupations + baseline skill panel.

        Uses permutation map to canonicalize code (avoids arbitrary alphabetical sorting) and
        queries riasec schema for matched jobs. If canonical profile not found, returns empty set.
        """
        repo = RiasecRepository(db)
        canonical_code = canonical_riasec(payload.riasec_code)
        profile = repo.get_profile(canonical_code)
        if profile:
            top_jobs = repo.top_matched_jobs(profile, limit=15)
            occupation_pool = [j.occ_code for j in top_jobs]
            top10_jobs = [
                {"onet_code": j.occ_code, "title": j.title} for j in top_jobs[:10]
            ]
        else:
            occupation_pool = []
            top10_jobs = []
        skills_panel = self._load_skill_definitions()
        return RiasecResult(
            riasec_code=canonical_code,
            occupation_pool=occupation_pool,
            top10_jobs=top10_jobs,  # type: ignore[arg-type]
            skills_panel=skills_panel,
        )

    # ---------------- Skill Weighting -----------------
    def compute_skill_weights(
        self, submission: SkillRatingsSubmission
    ) -> SkillWeightsResponse:
        """Compute adjusted weights from user ratings and baseline definitions.

        Algorithm (initial draft):
        - normalized_score = (raw_rating - dp20) / (dp80 - dp20), clipped 0..1
        - adjusted_weight = normalized_score * (1 + mid_gap_factor)
          where mid_gap_factor = (dp80 - dp50) / (dp80) to slightly boost skills with long tail of mastery.
        - category_weights: aggregate adjusted_weight by skill 'name' token root (simple placeholder grouping)
        """
        defs = {d.element_id: d for d in self._load_skill_definitions()}
        weighted: List[SkillWeighted] = []
        category_acc: Dict[str, float] = {}

        for element_id, raw in submission.ratings.items():
            skill_def = defs.get(element_id)
            if not skill_def:
                continue
            span = max(skill_def.data_point_80 - skill_def.data_point_20, 1e-6)
            normalized = (raw - skill_def.data_point_20) / span
            if normalized < 0:
                normalized = 0.0
            elif normalized > 1:
                normalized = 1.0
            mid_gap_factor = (skill_def.data_point_80 - skill_def.data_point_50) / max(skill_def.data_point_80, 1e-6)
            adjusted = normalized * (1 + mid_gap_factor)
            weighted.append(
                SkillWeighted(
                    element_id=element_id,
                    raw_rating=raw,
                    normalized_score=round(normalized, 4),
                    adjusted_weight=round(adjusted, 4),
                )
            )
            # Simple category key: first word of name
            cat_key = skill_def.name.split()[0]
            category_acc[cat_key] = category_acc.get(cat_key, 0.0) + adjusted

        # Normalize category weights to sum=1
        total_cat = sum(category_acc.values()) or 1.0
        category_weights_norm = {k: round(v / total_cat, 4) for k, v in category_acc.items()}

        return SkillWeightsResponse(
            riasec_code=submission.riasec_code,
            weighted_skills=sorted(weighted, key=lambda w: w.adjusted_weight, reverse=True),
            category_weights=category_weights_norm,
        )

    # ---------------- Backward compatibility placeholders -----------------
    def process_interest_quiz(self, payload: InterestQuizRequest) -> InterestQuizResponse:
        scores: Dict[str, float] = {"R": 8.5, "I": 7.0, "A": 6.0, "S": 5.0, "E": 4.0, "C": 3.0}
        return InterestQuizResponse(
            session_id="demo-session",
            top_codes=["RIA"],
            scores=scores,
        )

    def triage_skills(self) -> SkillTriageResponse:
        skills: List[Dict[str, object]] = [
            {"skill_id": "2.A.1.a", "name": "Active Listening", "frequency": 95},
            {"skill_id": "2.A.1.b", "name": "Critical Thinking", "frequency": 90},
        ]
        return SkillTriageResponse(skills=skills)
