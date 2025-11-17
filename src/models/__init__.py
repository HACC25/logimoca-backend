"""SQLAlchemy models for UH Pathfinder."""

# Base classes
from .base import Base, TimestampMixin, OnetBase

# TEMP: Only importing models actually needed for RIASEC endpoint
# to avoid relationship configuration errors
# Full model imports can be restored after fixing relationships

# RIASEC schema models (needed for assessment endpoint)
from .riasec_schema.riasec_profile import RiasecProfile
from .riasec_schema.interest_matched_job import InterestMatchedJob
try:
    # InterestFilteredSkill now stabilized; include for access when needed
    from .riasec_schema.interest_filtered_skill import InterestFilteredSkill
except ImportError:
    InterestFilteredSkill = None  # Graceful fallback if file sync glitch removes it

# Public schema models (needed for ingestion and pathways)
from .public_schema.sector import Sector
from .public_schema.institution import Institution
from .public_schema.pathway import Pathway
from .public_schema.program import Program
from .public_schema.occupation import Occupation
from .public_schema.associations import program_occupation_association

# O*NET schema models (for cross-schema relationships and skills/interests data)
from .onet_schema import OnetOccupation, Skill, Interest

# Client (Pydantic) models - if these exist
try:
    from .public_schema.interest_assessment import InterestAssessment
except ImportError:
    InterestAssessment = None
try:
    from .public_schema.skills_assessment import SkillsAssessment
except ImportError:
    SkillsAssessment = None

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "OnetBase",
    # RIASEC core models
    "RiasecProfile",
    "InterestMatchedJob",
    "InterestFilteredSkill",
    # Public schema models
    "Sector",
    "Institution",
    "Pathway",
    "Program",
    "Occupation",
    "program_occupation_association",
    # O*NET models
    "OnetOccupation",
    "Skill",
    "Interest",
    # Client models (if loaded)
    "InterestAssessment",
    "SkillsAssessment"
]