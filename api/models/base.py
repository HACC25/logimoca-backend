"""Base model configuration and mixins for SQLAlchemy models."""

from datetime import datetime
from typing import Any

from sqlalchemy import MetaData, event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# Naming convention for constraints and indexes
convention = {
    "ix": "ix_%(column_0_label)s",  # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
    "pk": "pk_%(table_name)s"  # Primary key
}

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    
    @declared_attr
    def created_at(self) -> Mapped[datetime]:
        """Timestamp for when the record was created."""
        return mapped_column(default=datetime.utcnow, nullable=False)
    
    @declared_attr
    def updated_at(self) -> Mapped[datetime]:
        """Timestamp for when the record was last updated."""
        return mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Base(DeclarativeBase):
    """Single declarative base for all models (app + onet)."""
    metadata = MetaData(naming_convention=convention)
    session: Session = None
    def __repr__(self) -> str:
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                attrs.append(f"{key}={value!r}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"


class OnetBase(Base):
    """Alias/abstract base for O*NET models; shares registry with Base."""
    __abstract__ = True

@event.listens_for(Session, 'after_attach')
def receive_after_attach(session: Session, instance: Any) -> None:
    """Set the session on the instance after it's attached to a session."""
    if isinstance(instance, Base):
        instance.session = session