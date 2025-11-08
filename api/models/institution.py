"""Institution model representing educational institutions and locations."""

from typing import List, Optional
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Institution(Base):
    """Educational institution in Hawai'i."""
    
    __tablename__ = "institutions"
    
    # Primary Key
    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    
    # Attributes
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(
        String(20), 
        nullable=False,
        comment="'4-year' | '2-year' | 'vocational'"
    )
    location: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="'Oʻahu' | 'Maui' | 'Big Island' | etc."
    )
    campus: Mapped[str | None] = mapped_column(String(100))
    website_url: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_email: Mapped[str | None] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    
    # Relationships
    programs: Mapped[List["Program"]] = relationship(
        back_populates="institution",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        """Return string representation of the Institution."""
        return f"Institution(id={self.id!r}, name={self.name!r}, type={self.type!r})"