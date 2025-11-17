from sqlalchemy import Integer, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, DOUBLE_PRECISION
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class VectorChunk(Base):
    __tablename__ = "vector_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Chunk content and embedding
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    # Store as double precision[] (no pgvector extension required).
    # Can be migrated to pgvector later without data loss.
    chunk_embedding: Mapped[list[float]] = mapped_column(ARRAY(DOUBLE_PRECISION()), nullable=False)

    # Source info: we store chunks for programs for now, but keep generic for future
    chunk_source_type: Mapped[str] = mapped_column(String(50), nullable=False, default="program")
    chunk_source_id: Mapped[str] = mapped_column(ForeignKey("programs.id"), nullable=False)

    # Extra metadata about the chunk
    chunk_metadata: Mapped[dict] = mapped_column(JSONB, nullable=True)