from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .skill import Skill
    from .onet_occupation import OnetOccupation
    from .program import Program

class Occupation(TimestampMixin, Base):
    __tablename__ = "occupation"
    # defaults to 'public' schema, * NOT ONET *

    # --- PK/FK ---
    # Primary Key AND a Foreign Key to the 'onet' schema
    onet_code: Mapped[str] = mapped_column(
        ForeignKey("onet.occupation_data.onetsoc_code"), 
        primary_key=True
    )

    
    # --- PATHFINDER APP FIELDS (EXTENDS O*NET DATA) ---
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

    
    # JSON fields
    interest_codes: Mapped[List[str]] = mapped_column(
        JSONB, 
        default=list,
        comment="RIASEC codes ordered by relevance"
    )
    interest_scores: Mapped[Dict[str, float]] = mapped_column(
        JSONB, 
        default=dict,
        comment="RIASEC scores (0-100) keyed by code"
    )
    top_skills: Mapped[List[Dict]] = mapped_column(
        JSONB, 
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
        "Program",
        secondary="program_occupation_association",
        back_populates="occupations"
    )
    # Skills relationship: Skill table already has onetsoc_code FK
    # Access via onet_occupation.skills or query Skill directly
    
    def _onet_occupation():  # late import to avoid circular during annotation processing
        from .onet_occupation import OnetOccupation
        return OnetOccupation

    onet_occupation: Mapped["OnetOccupation"] = relationship(
        _onet_occupation,
        back_populates="app_data",
        uselist=False  # one-to-one
    )

    # Indexes
    __table_args__ = (
        # GIN index for JSONB; default jsonb_ops is fine
        Index("idx_occupation_interest", "interest_codes", postgresql_using="gin"),
        Index("idx_occupation_job_zone", "job_zone")
    )
    
    def __repr__(self) -> str:
        return f"Occupation(onet_code={self.onet_code!r}, job_zone={self.job_zone!r})"