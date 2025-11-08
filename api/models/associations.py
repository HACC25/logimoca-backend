"""Association tables for many-to-many relationships."""

from datetime import datetime
from sqlalchemy import Table, Column, String, Float, DateTime, ForeignKey

from .base import Base

# Association table for Occupation <-> Skill relationship
occupation_skill = Table(
    "occupation_skill",
    Base.metadata,
    Column(
        "occupation_onet_code",
        String(10),
        ForeignKey("occupations.onet_code", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "skill_onet_element_id",
        String(10),
        ForeignKey("skills.onet_element_id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "importance",
        Float,
        nullable=False,
        comment="O*NET importance rating (1-5)"
    ),
    Column(
        "level",
        Float,
        nullable=False,
        comment="O*NET level rating (0-7)"
    )
)

# Association table for Program <-> Occupation relationship
program_occupation = Table(
    "program_occupation",
    Base.metadata,
    Column(
        "program_id",
        String(50),
        ForeignKey("programs.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "occupation_onet_code",
        String(10),
        ForeignKey("occupations.onet_code", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "confidence",
        Float,
        nullable=False,
        default=1.0,
        comment="Confidence score for program-occupation match (0-1)"
    ),
    Column(
        "created_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="Timestamp when the association was created"
    )
)