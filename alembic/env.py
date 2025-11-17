import os
import sys
import pathlib
from dotenv import load_dotenv, dotenv_values
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

# Add src to path so we can import models
_project_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_project_root))

# Import Base from models package - this will import all models via __init__.py
from src.models import Base
from src.models.public_schema.sector import Sector
from src.models.public_schema.pathway import Pathway
from src.models.public_schema.institution import Institution
from src.models.public_schema.interest_code import InterestCode
from src.models.public_schema.hs_skill import HSSkill
from src.models.public_schema.occupation import Occupation
from src.models.public_schema.program import Program
from src.models.public_schema.associations import program_occupation_association

target_metadata = Base.metadata

from alembic import context

# Load .env from project root (backend folder)
_env_file = _project_root / ".env"
load_dotenv(dotenv_path=_env_file)
if _env_file.exists():
    _cached_env = dotenv_values(_env_file)
else:
    raise RuntimeError("Could not load .env file for Alembic migrations.")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):
    """
    We want to IGNORE the 'onet' and 'riasec' schemas.
    """
    if type_ == "table" and object.schema not in (None, 'public'):
        # If the object is a table and its schema is NOT public, ignore it.
        return False

    # Otherwise, include all other objects (columns, indexes, etc.)
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    env_url = os.getenv("DATABASE_URL") or os.getenv("TEST_DATABASE_URL")
    if not env_url and _env_file.exists():
        env_url = _cached_env.get("DATABASE_URL") or _cached_env.get("TEST_DATABASE_URL")
    url = env_url or config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Prefer DATABASE_URL from environment/dotenv over alembic.ini placeholder
    section = config.get_section(config.config_ini_section, {})
    env_url = os.getenv("DATABASE_URL") or os.getenv("TEST_DATABASE_URL")
    if not env_url and _env_file.exists():
        env_url = _cached_env.get("DATABASE_URL") or _cached_env.get("TEST_DATABASE_URL")
    url = env_url or section.get("sqlalchemy.url")
    
    # Debug: print what URL we're using
    print(f"[Alembic] Using DATABASE_URL: {url}")
    
    if url:
        section["sqlalchemy.url"] = url
        
    connectable = engine_from_config(
        section,  # Use the modified section, not a fresh get_section call
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True 
        )
        

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
