"""Skill model representing O*NET skills with task statements and anchors."""

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import OnetBase

if TYPE_CHECKING:
    from .onet_occupation import OnetOccupation
    from .content_model_reference import ContentModelReference
    from .occupation import Occupation
    from .scale import ScaleReference

# In models/skill.py (REVISED)
class Skill(OnetBase):
    __tablename__ = "skills" # Maps to the 'skills' table 
    
    # --- ADD THIS ---
    __table_args__ = {"schema": "onet"}

    # --- Composite Primary Key ---
    onetsoc_code: Mapped[str] = mapped_column(
        ForeignKey("onet.occupation_data.onetsoc_code"), primary_key=True
    )
    element_id: Mapped[str] = mapped_column(
        ForeignKey("onet.content_model_reference.element_id"), primary_key=True
    )
    scale_id: Mapped[str] = mapped_column(
        ForeignKey("onet.scales_reference.scale_id"), primary_key=True
    )
    
    # --- The Score ---
    data_value: Mapped[float] = mapped_column(Float, nullable=False) # 
    
    # --- Relationships ---
    occupation: Mapped["OnetOccupation"] = relationship("OnetOccupation", back_populates="skills")
    element: Mapped["ContentModelReference"] = relationship("ContentModelReference", back_populates="skills")
    scale: Mapped["ScaleReference"] = relationship("ScaleReference")
    
    def __repr__(self) -> str:
        """Return string representation of the Skill."""
        return f"Skill(onet_element_id={self.onet_element_id!r}, name={self.name!r}, category={self.category!r})"