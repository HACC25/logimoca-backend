from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import OnetBase

if TYPE_CHECKING:
    from .scale import ScaleReference
    from .onet_occupation import OnetOccupation
    from .content_model_reference import ContentModelReference

class Interest(OnetBase):
    __tablename__ = "interests" # Maps to the 'interests' table 
    
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
    onet_occupation: Mapped["OnetOccupation"] = relationship(back_populates="interests")
    element: Mapped["ContentModelReference"] = relationship(back_populates="interests")
    scale: Mapped["ScaleReference"] = relationship()