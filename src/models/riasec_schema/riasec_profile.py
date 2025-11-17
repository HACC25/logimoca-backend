from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interest_matched_job import InterestMatchedJob
    from .interest_filtered_skill import InterestFilteredSkill

class RiasecProfile(Base):
    __tablename__ = "riasec_profiles"
    __table_args__ = {"schema": "riasec"}

    # Primary Key
    code: Mapped[str] = mapped_column(String, primary_key=True)

    # --- Relationships ---
    
    # One-to-Many: One RiasecProfile has ~150 matched jobs
    matched_jobs: Mapped[List["InterestMatchedJob"]] = relationship(
        back_populates="riasec_profile"
    )

    # One-to-Many: One RiasecProfile has 40 pre-scored skills
    filtered_skills: Mapped[List["InterestFilteredSkill"]] = relationship(
        back_populates="riasec_profile"
    )

    def __repr__(self) -> str:
        return f"RiasecProfile(code={self.code!r})"