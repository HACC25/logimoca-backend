"""Sector model representing career pathway industry domains."""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, TimestampMixin

if TYPE_CHECKING:
    from .pathway import Pathway

class Sector(TimestampMixin, Base):
    """Career pathway sector (industry domain)."""
    
    __tablename__ = "sectors"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    # Attributes
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_url: Mapped[str | None] = mapped_column(String(500))  # Optional field
    pathway_url: Mapped[str] = mapped_column(String(500), nullable=False)
    

    # One-to-Many: A Sector has many Pathways
    pathways: Mapped[List["Pathway"]] = relationship(
        back_populates="sector",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Return string representation of the Sector."""
        return f"Sector(id={self.id!r}, name={self.name!r})"