from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import OnetBase

if TYPE_CHECKING:
    pass

class ScaleReference(OnetBase):
    __tablename__ = "scales_reference"
    __table_args__ = {"schema": "onet"}
    
    scale_id: Mapped[str] = mapped_column(String(3), primary_key=True)
    scale_name: Mapped[str] = mapped_column(String(50), nullable=False)