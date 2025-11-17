"""InterestFilteredSkill model for pre-scored skills by RIASEC profile."""

from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base

if TYPE_CHECKING:
    from .riasec_profile import RiasecProfile


class InterestFilteredSkill(Base):
    """
    Pre-scored skills for each RIASEC profile.
    Each RIASEC code has skills ranked by frequency/relevance.
    """
    __tablename__ = "interest_filtered_skills"
    __table_args__ = {"schema": "riasec"}

    # --- Composite Primary Key ---
    # Assuming a skill can only appear once per profile
    
    skill_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    
    fk_riasec_code: Mapped[str] = mapped_column(
        ForeignKey("riasec.riasec_profiles.code"), primary_key=True
    )
    
    # --- Data ---
    frequency: Mapped[int] = mapped_column(BigInteger)
    
    # --- Relationships ---
    
    # Many-to-One: This skill score belongs to one RiasecProfile
    riasec_profile: Mapped["RiasecProfile"] = relationship(
        back_populates="filtered_skills"
    )

    def __repr__(self) -> str:
        return f"InterestFilteredSkill(riasec_code={self.fk_riasec_code!r}, skill_id={self.skill_id!r}, frequency={self.frequency})"
