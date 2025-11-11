from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin
from .content_model_reference import ContentModelReference

if TYPE_CHECKING:
    pass

class HSSkill(TimestampMixin, Base):
    __tablename__ = "app_skills" # This table lives in 'public'
    
    # This links our app skill to the master O*NET definition
    onet_element_id: Mapped[str] = mapped_column(
        ForeignKey("onet.content_model_reference.element_id"), primary_key=True
    )
    
    # --- Custom High-School Adjusted Skills ---
    task_statement: Mapped[str] = mapped_column(Text)
    anchor_low: Mapped[str] = mapped_column(Text)
    anchor_high: Mapped[str] = mapped_column(Text)
    
    # Relationship to the O*NET definition
    onet_definition: Mapped["ContentModelReference"] = relationship()