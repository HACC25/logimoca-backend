"""SQLAlchemy models for UH Pathfinder."""

# Base classes
from .base import Base, TimestampMixin, OnetBase

# O*NET schema models
from .onet_occupation import OnetOccupation
from .content_model_reference import ContentModelReference
from .job_zone_reference import JobZoneReference
from .scale import ScaleReference
from .interest import Interest

# Public schema models (app-specific)
from .sector import Sector
from .institution import Institution
from .program import Program
from .occupation import Occupation
from .skill import Skill
from .interest_code import InterestCode
from .hs_skill import HSSkill

# Association tables
from .associations import (
    program_occupation_association
)

# Client (Pydantic) models
from .client_models import InterestAssessment, SkillsAssessment

__all__ = [
    # Base
    "Base",
    "TimestampMixin",
    "OnetBase",
    # O*NET models
    "OnetOccupation",
    "ContentModelReference",
    "JobZoneReference",
    "ScaleReference",
    "Interest",
    # App models
    "Sector",
    "Institution",
    "Program",
    "Occupation",
    "Skill",
    "InterestCode",
    "HSSkill",
    # Associations
    "program_occupation_association",
    # Client models
    "InterestAssessment",
    "SkillsAssessment"
]