"""Tests for cross-schema relationships between O*NET and app models.

This module dynamically queries existing O*NET rows instead of relying on
hardcoded SOC codes or element IDs. It then creates app-side extension rows
and validates relationships without mutating O*NET reference data.
"""

import logging
import os
from pathlib import Path
from typing import Iterator, Tuple

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker, joinedload

from dotenv import load_dotenv

from api.models.base import Base
from api.models.onet_occupation import OnetOccupation
from api.models.content_model_reference import ContentModelReference
from api.models.occupation import Occupation
from api.models.hs_skill import HSSkill
from api.models.program import Program
from api.models.sector import Sector
from api.models.institution import Institution
from api.models.interest_code import InterestCode
from api.models.associations import program_occupation_association

logger = logging.getLogger(__name__)

tests_dir = Path(__file__).parent.parent
load_dotenv(tests_dir / ".env")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fetch_existing_onet_data(db_session: Session) -> Tuple[OnetOccupation, ContentModelReference]:
    """Pick one occupation and one content model element from loaded O*NET data.

    Skips tests if data isn't loaded.
    """
    occ = db_session.query(OnetOccupation).order_by(OnetOccupation.onet_code).first()
    if occ is None:
        pytest.skip("No O*NET occupations present. Load O*NET data before running tests.")
    elem = db_session.query(ContentModelReference).order_by(ContentModelReference.element_id).first()
    if elem is None:
        pytest.skip("No O*NET content model reference rows present. Load O*NET data.")
    return occ, elem

def build_app_occupation(onet_code: str) -> Occupation:
    return Occupation(
        onet_code=onet_code,
        median_annual_wage=120000.0,
        employment_outlook="Bright",
        job_zone=4,
        interest_codes=["I", "C"],
        interest_scores={"I": 85.0, "C": 40.0},
        top_skills=[{"name": "Programming", "importance": 90}],
        onet_url=f"https://www.onetonline.org/link/summary/{onet_code}"
    )

def build_hs_skill(element_id: str) -> HSSkill:
    return HSSkill(
        onet_element_id=element_id,
        task_statement="Listen actively in class.",
        anchor_low="Interrupts frequently",
        anchor_high="Summarizes key points"
    )

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def engine():
    db_url = os.getenv("TEST_DATABASE_URL") or os.getenv("DATABASE_URL")
    if not db_url:
        pytest.skip("TEST_DATABASE_URL or DATABASE_URL not set; skipping schema tests.")
    eng = create_engine(db_url, echo=False)
    Base.metadata.create_all(
        eng,
        tables=[
            Sector.__table__,
            Institution.__table__,
            Program.__table__,
            Occupation.__table__,
            HSSkill.__table__,
            InterestCode.__table__,
            program_occupation_association,
        ],
        checkfirst=True,
    )
    return eng

@pytest.fixture(scope="module")
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture
def db_session(session_factory) -> Iterator[Session]:
    session = session_factory()
    try:
        if session.bind and session.bind.dialect.name == "postgresql":
            session.execute(text("SET search_path TO onet, public"))
        yield session
    finally:
        session.rollback()
        session.close()

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_cross_schema_relationships(db_session, caplog):
    caplog.set_level(logging.INFO)
    logger.info("Starting dynamic cross-schema relationship test")

    onet_occ, content_ref = fetch_existing_onet_data(db_session)
    app_occ = build_app_occupation(onet_occ.onet_code)
    hs_skill = build_hs_skill(content_ref.element_id)

    db_session.add_all([app_occ, hs_skill])
    db_session.flush()  # rollback will clean these

    retrieved_app_occ = (
        db_session.query(Occupation)
        .filter_by(onet_code=app_occ.onet_code)
        .options(joinedload(Occupation.onet_occupation))
        .first()
    )
    retrieved_hs_skill = (
        db_session.query(HSSkill)
        .filter_by(onet_element_id=hs_skill.onet_element_id)
        .options(joinedload(HSSkill.onet_definition))
        .first()
    )

    assert retrieved_app_occ is not None
    assert retrieved_app_occ.onet_occupation is not None
    assert retrieved_app_occ.onet_occupation.onet_code == onet_occ.onet_code
    assert retrieved_app_occ.onet_occupation.title == onet_occ.title
    assert len(retrieved_app_occ.onet_occupation.description) >= 5
    assert retrieved_app_occ.interest_codes == ["I", "C"]
    assert retrieved_app_occ.interest_scores["I"] == 85.0

    assert retrieved_hs_skill is not None
    assert retrieved_hs_skill.onet_definition.element_id == content_ref.element_id
    assert retrieved_hs_skill.onet_definition.element_name == content_ref.element_name

    missing_occ = db_session.query(Occupation).filter_by(onet_code="00-0000.00").first()
    assert missing_occ is None

    missing_skill = db_session.query(HSSkill).filter_by(onet_element_id="X.Y.Z").first()
    assert missing_skill is None

    logger.info("Cross-schema dynamic relationship test passed")

def test_repr_methods(db_session):
    onet_occ, _ = fetch_existing_onet_data(db_session)
    text_repr = repr(onet_occ)
    assert onet_occ.onet_code in text_repr
    assert onet_occ.title.split()[0] in text_repr

def test_one_to_one_link(db_session):
    """Validate reciprocal access between app Occupation and OnetOccupation."""
    onet_occ, _ = fetch_existing_onet_data(db_session)
    app_occ = build_app_occupation(onet_occ.onet_code)
    db_session.add(app_occ)
    db_session.flush()

    # Forward
    assert app_occ.onet_occupation is not None
    assert app_occ.onet_occupation.onet_code == onet_occ.onet_code
    # Reverse
    assert onet_occ.app_data is not None
    assert onet_occ.app_data.onet_code == app_occ.onet_code
