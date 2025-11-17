from datetime import datetime
from typing import List, Dict, TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, TimestampMixin

if TYPE_CHECKING:
    from .content_model_reference import ContentModelReference


class AppSkill(TimestampMixin, Base):
    __tablename__ = "app_skills" # This table lives in 'public'
    
    # This links our app skill to the master O*NET definition
    onet_element_id: Mapped[str] = mapped_column(
        ForeignKey("onet.content_model_reference.element_id"), primary_key=True
    )

    is_high_school_adjusted: Mapped[bool] = mapped_column(nullable=False, default=False)

    element_name: Mapped[str] = mapped_column(String(150), nullable=False)
    data_point_20: Mapped[float] = mapped_column(Float, nullable=False)
    data_point_35: Mapped[float] = mapped_column(Float, nullable=False)
    data_point_50: Mapped[float] = mapped_column(Float, nullable=False)
    data_point_65: Mapped[float] = mapped_column(Float, nullable=False)
    data_point_80: Mapped[float] = mapped_column(Float, nullable=False)
    
    anchor_first: Mapped[str] = mapped_column(Text, nullable=False)
    anchor_second: Mapped[str] = mapped_column(Text, nullable=True)
    anchor_third: Mapped[str] = mapped_column(Text, nullable=True)
    anchor_fourth: Mapped[str] = mapped_column(Text, nullable=True)
    anchor_last: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Relationship to the O*NET definition
    onet_definition: Mapped["ContentModelReference"] = relationship()
    
"""
"ElementId": "2.C.1.a",
        "ElementName": "Administration and Management",
        "DataPoint20": 1.534,
        "DataPoint35": 2.4145,
        "DataPoint50": 3.295,
        "DataPoint65": 4.1755,
        "DataPoint80": 5.056,
        "AnchorFirst": "Complete a timesheet",
        "AnchorSecond": "",
        "AnchorThrid": "Monitor project progress to complete it on time",
        "AnchorFourth": "",
        "AnchorLast": "Manage a $10m company",
        "Question": "How much do you know about business planning and leadership?",
        "EasyReadDescription": "Knowledge of business and management principles involved in strategic planning, resource allocation, human resources modeling, leadership technique, production methods, and coordination of people and resources."
"""