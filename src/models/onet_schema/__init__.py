"""O*NET schema models."""

from .onet_occupation import OnetOccupation
from .skill import Skill
from .interest import Interest
from .content_model_reference import ContentModelReference
from .scale import ScaleReference
from .interest import Interest
from .job_zone_reference import JobZoneReference

__all__ = [
    "OnetOccupation",
    "Skill",
    "Interest",
    "ContentModelReference",
    "ScaleReference",
    "Interest",
    "JobZoneReference",
]
