# In models/pathway.py
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .sector import Sector
    from .program import Program

class Pathway(Base):
    """
    Represents a specific career pathway within a broader Sector.
    (e.g., "Animal Systems" within "Agriculture")
    """
    __tablename__ = "pathways"
    # This table lives in the 'public' schema by default

    # ID concatenated to appropriately represent HI Careers data (e.g., "AFNRM-animalsystems")
    id: Mapped[str] = mapped_column(String(100), primary_key=True) 
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    pathway_url: Mapped[str | None] = mapped_column(String(500))

    # --- Relationships ---
    
    # Foreign Key to Sector
    sector_id: Mapped[str] = mapped_column(ForeignKey("sectors.id"), index=True)

    # Many-to-One: A Pathway belongs to one Sector
    sector: Mapped["Sector"] = relationship(back_populates="pathways")
    
    # One-to-Many: A Pathway has many Programs
    programs: Mapped[List["Program"]] = relationship(
        back_populates="pathway",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Pathway(id={self.id!r}, name={self.name!r})"