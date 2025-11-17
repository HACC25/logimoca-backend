"""App-specific high school skill wrapper linked to O*NET content model element.

Public schema model that references onet.content_model_reference.element_id and
stores app-facing anchors/task statement.
"""
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class HSSkill(Base):
    __tablename__ = "hs_skill"
    # defaults to public schema

    # Primary Key that is also a FK to O*NET element
    onet_element_id: Mapped[str] = mapped_column(
        ForeignKey("onet.content_model_reference.element_id"), primary_key=True
    )

    # App-specific descriptive fields
    task_statement: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_low: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_high: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationship back to the O*NET reference row
    onet_definition = relationship(
        "ContentModelReference",
        primaryjoin="HSSkill.onet_element_id == ContentModelReference.element_id",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"HSSkill(onet_element_id={self.onet_element_id!r})"
