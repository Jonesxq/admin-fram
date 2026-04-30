import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import make_url
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.models.base import Base
from app.models import system  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def reject_in_memory_database_url(url: str) -> None:
    parsed_url = make_url(url)
    is_sqlite = parsed_url.drivername.startswith("sqlite")
    database = parsed_url.database
    is_in_memory = (
        is_sqlite
        and (
            database in (None, "", ":memory:")
            or database.startswith("file::memory:")
            or parsed_url.query.get("mode") == "memory"
        )
    )
    if is_in_memory and os.getenv("ALLOW_IN_MEMORY_ALEMBIC") != "1":
        raise RuntimeError(
            "Refusing to run Alembic against an in-memory SQLite database. "
            "Set ALLOW_IN_MEMORY_ALEMBIC=1 only for explicit migration tests.",
        )


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    reject_in_memory_database_url(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    reject_in_memory_database_url(config.get_main_option("sqlalchemy.url"))
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
