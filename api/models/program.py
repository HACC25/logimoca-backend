"""Program model representing UH training programs."""

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING, Optional

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.ext.declarative import declared_attr

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .institution import Institution
    from .occupation import Occupation
    from .pathway import Pathway

class Program(TimestampMixin, Base):
    """Training program at any institution."""
    __tablename__ = "programs"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    # Foreign Keys with cascade delete
    pathway_id: Mapped[str] = mapped_column(ForeignKey("pathways.id"), index=True)
    institution_id: Mapped[str] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)

    @validates("pathway_id", "institution_id")
    def validate_foreign_key(self, key: str, value: str) -> str:
        """Validate a foreign key reference exists."""
        if not value:
            raise ValueError(f"{key} is required")
            
        if key == "pathway_id":
            if not isinstance(value, str):
                raise ValueError("Pathway ID must be a string")
        elif key == "institution_id":
            if not isinstance(value, str):
                raise ValueError("Institution ID must be a string")
        return value
    
    # Attributes
    name: Mapped[str] = mapped_column(String(500))
    degree_type: Mapped[str] = mapped_column(
        String(50),
        comment="'Certificate' | 'Associate' | 'Bachelor' | 'Master' | 'Doctorate'"
    )
    duration_years: Mapped[float] = mapped_column(Float)
    total_credits: Mapped[int] = mapped_column(Integer)
    cost_per_credit: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    program_url: Mapped[str] = mapped_column(String(500))
    # JSON fields
    prerequisites: Mapped[List[str]] = mapped_column(JSON, default=list)
    delivery_modes: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # Relationships
    pathway: Mapped["Pathway"] = relationship(back_populates="programs")
    institution: Mapped["Institution"] = relationship(back_populates="programs")
    occupations: Mapped[List["Occupation"]] = relationship(
        secondary="program_occupation_association",
        back_populates="programs"
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_program_pathway", "pathway_id"),
        Index("idx_program_duration", "duration_years"),
    )
    
    def __repr__(self) -> str:
        """Return string representation of the Program."""
        return f"Program(id={self.id!r}, name={self.name!r}, degree_type={self.degree_type!r})"