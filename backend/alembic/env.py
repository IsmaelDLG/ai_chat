from logging.config import fileConfig
import asyncio

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from app.core.config import get_settings
from app.dataaccess.db import Base

import app.dataaccess.models

settings = get_settings()

config = context.config

# Establece la URL de asyncpg directamente
config.set_main_option(
    "sqlalchemy.url", 
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Renderiza tipos enum y tipos personalizados correctamente
        render_as_batch=False 
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_offline() -> None:
    # Usamos la misma URL pero síncrona/limpia si ejecutas offline
    url = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    # Creamos el engine pasando la configuración explícita
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()