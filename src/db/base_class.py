"""Expose SQLAlchemy Base from the models package for centralized imports."""

from models.base import Base  # re-export Base used across the app

__all__ = ["Base"]
