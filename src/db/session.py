"""SQLAlchemy session/engine setup and FastAPI dependency.

Reads DATABASE_URL from core.config.settings. Sets search_path for onet,public
when connecting to Postgres to enable cross-schema queries.
"""
from contextlib import contextmanager
from typing import Iterator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings


_engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None


def get_engine() -> Engine:
	global _engine, SessionLocal
	if _engine is None:
		_engine = create_engine(settings.database_url, future=True)
		SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, class_=Session)
	return _engine


def get_session_factory() -> sessionmaker:
	if SessionLocal is None:
		get_engine()
	assert SessionLocal is not None
	return SessionLocal


def _maybe_set_search_path(db: Session) -> None:
	try:
		bind = db.get_bind()
		if bind and bind.dialect.name == "postgresql":
			db.execute(text("SET search_path TO onet, public"))
	except Exception:
		# Non-fatal; continue without schema adjustment
		pass


@contextmanager
def session_scope() -> Iterator[Session]:
	"""Provide a transactional scope around a series of operations."""
	SessionFactory = get_session_factory()
	db = SessionFactory()
	try:
		_maybe_set_search_path(db)
		yield db
		db.commit()
	except Exception:
		db.rollback()
		raise
	finally:
		db.close()


def get_db() -> Iterator[Session]:
	"""FastAPI dependency that yields a DB session and ensures cleanup."""
	with session_scope() as db:
		yield db
