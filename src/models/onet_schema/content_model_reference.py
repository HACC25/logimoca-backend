from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import OnetBase

if TYPE_CHECKING:
    from .skill import Skill
    from .interest import Interest

class ContentModelReference(OnetBase):
    __tablename__ = "content_model_reference"
    __table_args__ = {"schema": "onet"}
    
    # Primary Key
    element_id: Mapped[str] = mapped_column(String(20), primary_key=True) # CHANGED
    
    element_name: Mapped[str] = mapped_column(String(150), nullable=False) # 
    description: Mapped[str] = mapped_column(Text, nullable=False) # 


    
    # --- This model defines all skills, interests ---
    skills: Mapped[List["Skill"]] = relationship("Skill", back_populates="element")
    interests: Mapped[List["Interest"]] = relationship("Interest", back_populates="element")