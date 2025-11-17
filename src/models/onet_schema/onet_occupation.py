"""Occupation model representing O*NET occupations."""

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import OnetBase

if TYPE_CHECKING:
    from ..public_schema.occupation import Occupation
    from .skill import Skill
    from .interest import Interest

class OnetOccupation(OnetBase):
    """O*NET occupation with associated career data."""
    __tablename__ = "occupation_data" # from loaded O*NET schema
    __table_args__ = {"schema": "onet"}
    
    # Primary Key (O*NET SOC code)
    # Map Python attribute 'onet_code' to database column 'onetsoc_code'
    onet_code: Mapped[str] = mapped_column("onetsoc_code", String(10), primary_key=True)
    
    # Attributes
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # --- Relationships ---
    
    # One-to-One: Link to public.occupation (Pathfinder app extensions).
    # String reference avoids circular import; foreign() explicitly marks the remote side.
    app_data: Mapped["Occupation"] = relationship(
        "Occupation",
        back_populates="onet_occupation",
        uselist=False
    )

    # O*NET Relationships - now using simple string references since models imported in package
    skills: Mapped[List["Skill"]] = relationship(
        "Skill",
        back_populates="onet_occupation"
    )
    interests: Mapped[List["Interest"]] = relationship(
        "Interest",
        back_populates="onet_occupation"
    )
    
    # ... other relationships for abilities, knowledge, etc.

    
    def __repr__(self) -> str:
        """Return string representation of the Occupation."""
        return f"Occupation(onet_code={self.onet_code!r}, title={self.title!r})"