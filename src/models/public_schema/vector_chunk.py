from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TSVECTOR

from typing import Any
from ..base import Base


class VectorChunk(Base):
    __tablename__ = "program_vector_chunks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("scraped_program_source.program_id"))
    text_chunk: Mapped[str] = mapped_column(Text, nullable=False)
    vector: Mapped[Any] = mapped_column(TSVECTOR) # Using a pgvector type