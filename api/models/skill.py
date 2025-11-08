"""Skill model representing O*NET skills with task statements and anchors."""

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .occupation import Occupation

class Skill(Base):
    """O*NET skill element with task statements and rating anchors."""
    __tablename__ = "skills"
    
    # Primary Key
    onet_element_id: Mapped[str] = mapped_column(
        String(10), 
        primary_key=True,
        comment="O*NET element ID for the skill"
    )
    
    # Attributes
    name: Mapped[str] = mapped_column(
        String(200), 
        nullable=False,
        comment="Name of the skill"
    )
    category: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="Skill category from O*NET taxonomy"
    )
    task_statement: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Description of how the skill is applied"
    )
    anchor_low: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Description of low skill level"
    )
    anchor_high: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        comment="Description of high skill level"
    )
    
    # Global triage data
    mean_importance: Mapped[float | None] = mapped_column(
        Float,
        comment="Average importance score across occupations"
    )
    mean_level: Mapped[float | None] = mapped_column(
        Float,
        comment="Average required level across occupations"
    )
    
    # Relationships
    occupations: Mapped[List["Occupation"]] = relationship(
        secondary="occupation_skill",
        back_populates="skills"
    )
    
    def __repr__(self) -> str:
        """Return string representation of the Skill."""
        return f"Skill(onet_element_id={self.onet_element_id!r}, name={self.name!r}, category={self.category!r})"