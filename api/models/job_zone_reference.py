
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import OnetBase

if TYPE_CHECKING:
    pass

class JobZoneReference(OnetBase):
    """Reference table for O*NET Job Zone definitions."""
    __tablename__ = "job_zone_reference"
    __table_args__ = {"schema": "onet"}
    
    # Primary Key
    job_zone: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Attributes
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    environment: Mapped[str] = mapped_column(Text, nullable=False)
    education: Mapped[str] = mapped_column(Text, nullable=False)
    experience: Mapped[str] = mapped_column(Text, nullable=False)