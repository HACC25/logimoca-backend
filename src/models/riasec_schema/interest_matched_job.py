from sqlalchemy import String, ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from types import TYPE_CHECKING

if TYPE_CHECKING:
    from .riasec_profile import RiasecProfile

class InterestMatchedJob(Base):
    __tablename__ = "interest_matched_jobs"
    __table_args__ = {"schema": "riasec"}
    
    # --- Composite Primary Key ---
    # Assuming a job can only appear once per profile
    
    occ_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    
    fk_riasec_code: Mapped[str] = mapped_column(
        ForeignKey("riasec.riasec_profiles.code"), primary_key=True
    )

    # --- Data ---
    title: Mapped[str] = mapped_column(String(150))
    interests_count: Mapped[int] = mapped_column(BigInteger)
    interest_sum: Mapped[float] = mapped_column(Numeric)
    
    # --- Relationships ---
    
    # Many-to-One: This job match belongs to one RiasecProfile
    riasec_profile: Mapped["RiasecProfile"] = relationship(
        back_populates="matched_jobs"
    )