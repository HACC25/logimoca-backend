"""Program model representing UH training programs.

Mapper fix: ensure association table `program_occupation_association` is loaded before
relationship configuration by importing it explicitly. This avoids InvalidRequestError
when only Program is imported (e.g., ingestion scripts) without importing Occupation.
"""

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING, Optional

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.ext.declarative import declared_attr

from ..base import Base, TimestampMixin
from .associations import program_occupation_association  # explicit import ensures table exists

if TYPE_CHECKING:
    from .institution import Institution
    from .occupation import Occupation
    from .pathway import Pathway

class Program(TimestampMixin, Base):
    """Training program at any institution."""
    __tablename__ = "programs"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    
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
    program_links: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        default=list,
        comment="Additional URLs for program info, application, etc."
    )
    
    # Relationships
    pathway: Mapped["Pathway"] = relationship(back_populates="programs")
    institution: Mapped["Institution"] = relationship(back_populates="programs")
    # Many-to-Many: Programs related to Occupations via association table.
    # Using actual Table object ensures mapper can find it even if Occupation not imported yet.
    occupations: Mapped[List["Occupation"]] = relationship(
        "Occupation",
        secondary=program_occupation_association,
        back_populates="programs"
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now(),
        onupdate=datetime.now()
    )
    
    # Indexes
    __table_args__ = (
        Index("idx_program_pathway", "pathway_id"),
        Index("idx_program_duration", "duration_years"),
    )
    
    def __repr__(self) -> str:
        """Return string representation of the Program."""
        return f"Program(id={self.id!r}, name={self.name!r}, degree_type={self.degree_type!r})"