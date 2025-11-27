from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Alembic config
config = context.config
database_url = os.getenv("DATABASE_URL")
if database_url:
    print(f"DEBUG: Using DATABASE_URL = {database_url}")
    config.set_main_option("sqlalchemy.url", database_url)


from todo.db.base import Base
from todo.model.project import Project
from todo.model.task import Task

# metadata
target_metadata = Base.metadata

fileConfig(config.config_file_name)


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
