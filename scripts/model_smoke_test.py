"""Model smoke test: import key models and report mapping/table info.
Run: python3 scripts/model_smoke_test.py
"""
from sqlalchemy import inspect
from src.db.session import get_engine

problems = []

print("🔍 Starting model import smoke test")

try:
    from src.models.riasec_schema.riasec_profile import RiasecProfile
    from src.models.riasec_schema.interest_matched_job import InterestMatchedJob
    try:
        from src.models.riasec_schema.interest_filtered_skill import InterestFilteredSkill
    except ImportError as e:
        InterestFilteredSkill = None
        problems.append(f"InterestFilteredSkill missing: {e}")
except Exception as e:
    problems.append(f"RIASEC core import failure: {e}")

engine = get_engine()
inspector = inspect(engine)
print("Schemas available (may be subset):", inspector.get_schema_names())

for schema in ["riasec"]:
    try:
        tables = inspector.get_table_names(schema=schema)
        print(f"Schema '{schema}' tables: {tables}")
    except Exception as e:
        problems.append(f"Error listing tables for schema '{schema}': {e}")

if InterestFilteredSkill is not None:
    print("InterestFilteredSkill columns:", [c.name for c in InterestFilteredSkill.__table__.columns])
else:
    print("InterestFilteredSkill not imported (file may be missing)")

print("RiasecProfile columns:", [c.name for c in RiasecProfile.__table__.columns])
print("InterestMatchedJob columns:", [c.name for c in InterestMatchedJob.__table__.columns])

if problems:
    print("\n⚠️ Issues detected:")
    for p in problems:
        print(" -", p)
else:
    print("\n✅ All target models imported successfully")
