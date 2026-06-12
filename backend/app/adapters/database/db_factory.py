from app.adapters.database.base import BaseGameStore
from app.adapters.database.sqlite_db import SQLiteGameStore
from app.adapters.database.postgres_db import PostgresGameStore
from app.core.config import settings


def get_game_store() -> BaseGameStore:
    """
    Select database provider based on .env.

    Current:
    DATABASE_PROVIDER=sqlite

    Future:
    DATABASE_PROVIDER=postgres
    """

    provider = settings.database_provider.lower().strip()

    if provider == "sqlite":
        return SQLiteGameStore()

    if provider == "postgres":
        return PostgresGameStore()

    raise ValueError(f"Unsupported database provider: {settings.database_provider}")