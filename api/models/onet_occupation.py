"""Occupation model representing O*NET occupations."""

from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import OnetBase

if TYPE_CHECKING:
    from .occupation import Occupation
    from .program import Program
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

    # --- 1:1 FK (Foreign Key)for Occupation ---
    # Use a callable import to resolve cross-registry relationship without circular imports
    def _app_occupation():  # type: ignore[no-redef]
        from .occupation import Occupation
        return Occupation

    # Explicit primaryjoin: Occupation.onet_code (public) references this PK via FK.
    from sqlalchemy.orm import foreign
    app_data: Mapped["Occupation"] = relationship(
        _app_occupation,
        back_populates="onet_occupation",
        uselist=False,
        primaryjoin="OnetOccupation.onet_code == foreign(Occupation.onet_code)"
    )

    # O*NET Relationships
    skills: Mapped[List["Skill"]] = relationship(
        "Skill",
        foreign_keys="[Skill.onetsoc_code]",
        back_populates="occupation"
    )
    interests: Mapped[List["Interest"]] = relationship(
        "Interest",
        foreign_keys="[Interest.onetsoc_code]",
        back_populates="onet_occupation"
    )
    
    # ... other relationships for abilities, knowledge, etc.

    
    def __repr__(self) -> str:
        """Return string representation of the Occupation."""
        return f"Occupation(onet_code={self.onet_code!r}, title={self.title!r})"