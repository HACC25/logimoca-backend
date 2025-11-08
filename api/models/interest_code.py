"""InterestCode model representing RIASEC codes and metadata."""

import re
from typing import Dict
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from .base import Base

class InterestCode(Base):
    """RIASEC interest code with associated metadata."""
    __tablename__ = "interest_codes"
    
    # Primary Key
    code: Mapped[str] = mapped_column(
        String(1), 
        primary_key=True,
        comment="'R' | 'I' | 'A' | 'S' | 'E' | 'C'"
    )
    
    # Attributes
    name: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="Full name (e.g., 'Realistic', 'Investigative')"
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Detailed description of the interest type"
    )
    color_hex: Mapped[str] = mapped_column(
        String(7), 
        nullable=False,
        comment="Hex color code for UI theming (e.g., '#3B82F6')"
    )
    job_tasks: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Example tasks/activities for this interest type"
    )
    work_values: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Key work values associated with this type"
    )
    
    @validates('code')
    def validate_code(self, key, code):
        """Validate RIASEC code."""
        if not code or code not in "RIASEC":
            raise ValueError("Code must be one of R,I,A,S,E,C")
        return code

    @validates('color_hex')
    def validate_color(self, key, color):
        """Validate hex color code."""
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            raise ValueError("Color must be a valid hex code (e.g., #FF0000)")
        return color
    
    def __repr__(self) -> str:
        """Return string representation of the InterestCode."""
        return f"InterestCode(code={self.code!r}, name={self.name!r})"