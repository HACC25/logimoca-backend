"""Occupation model representing O*NET occupations."""

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .program import Program
    from .skill import Skill

class Occupation(Base):
    """O*NET occupation with associated career data."""
    __tablename__ = "occupations"
    
    # Primary Key (O*NET SOC code)
    onet_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    # Attributes
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Career info
    median_annual_wage: Mapped[float | None] = mapped_column(Float)
    employment_outlook: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="Growth outlook category from O*NET"
    )
    job_zone: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        comment="O*NET Job Zone (1-5 representing required preparation level)"
    )
    typical_education: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        comment="Typical education level required"
    )
    
    # JSON fields
    interest_codes: Mapped[List[str]] = mapped_column(
        JSON, 
        default=list,
        comment="RIASEC codes ordered by relevance"
    )
    interest_scores: Mapped[Dict[str, float]] = mapped_column(
        JSON, 
        default=dict,
        comment="RIASEC scores (0-100) keyed by code"
    )
    top_skills: Mapped[List[Dict]] = mapped_column(
        JSON, 
        default=list,
        comment="List of most important skills with scores"
    )
    
    # URLs
    onet_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Metadata
    last_updated: Mapped[datetime] = mapped_column(
        nullable=False, 
        default=datetime.utcnow
    )
    
    # Relationships
    programs: Mapped[List["Program"]] = relationship(
        secondary="program_occupation",
        back_populates="occupations"
    )
    skills: Mapped[List["Skill"]] = relationship(
        secondary="occupation_skill",
        back_populates="occupations"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_occupation_interest", "interest_codes", postgresql_using="gin"),
        Index("idx_occupation_job_zone", "job_zone")
    )
    
    def __repr__(self) -> str:
        """Return string representation of the Occupation."""
        return f"Occupation(onet_code={self.onet_code!r}, title={self.title!r}, job_zone={self.job_zone})"