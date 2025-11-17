# In models/scraped_data.py
from typing import TYPE_CHECKING
from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .program import Program

class ScrapedProgramSource(Base):
    __tablename__ = "scraped_program_source"
    
    # One-to-One relationship with Program
    program_id: Mapped[str] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), 
        primary_key=True
    )
    
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    scraped_url: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Link back to the Program object
    program: Mapped["Program"] = relationship(back_populates="source_text")