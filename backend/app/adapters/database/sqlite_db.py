import json
import sqlite3
from pathlib import Path

from app.adapters.database.base import BaseGameStore
from app.core.config import settings


class SQLiteGameStore(BaseGameStore):
    """
    SQLite persistent storage for Baymax games.
    """

    def __init__(self, db_path: str | None = None):
        self.db_path = self._resolve_db_path(db_path or settings.sqlite_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _resolve_db_path(self, raw_path: str) -> Path:
        path = Path(raw_path)

        if path.is_absolute():
            return path

        current_working_dir_candidate = Path.cwd() / path

        # file path:
        # backend/app/adapters/database/sqlite_db.py
        backend_root = Path(__file__).resolve().parents[3]
        project_root = Path(__file__).resolve().parents[4]

        candidates = [
            current_working_dir_candidate,
            backend_root / path,
            project_root / path,
        ]

        # For DB, file may not exist yet. Prefer backend/app/storage path.
        for candidate in candidates:
            if candidate.parent.exists():
                return candidate

        return backend_root / path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    white_agent_id TEXT NOT NULL,
                    black_agent_id TEXT NOT NULL,
                    white_agent_name TEXT,
                    black_agent_name TEXT,
                    move_count INTEGER DEFAULT 0,
                    result TEXT,
                    reason TEXT,
                    game_json TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def health_check(self) -> dict:
        try:
            with self._connect() as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM games")
                count = cursor.fetchone()[0]

            return {
                "ok": True,
                "provider": "sqlite",
                "path": str(self.db_path),
                "games_count": count,
            }

        except Exception as exc:
            return {
                "ok": False,
                "provider": "sqlite",
                "path": str(self.db_path),
                "error": str(exc),
            }

    def save_game(self, game: dict) -> dict:
        state = game["state"]
        game_status = state.get("game_status", {})

        game_id = game["game_id"]
        created_at = game["created_at"]
        updated_at = game["updated_at"]
        white_agent_id = game["white_agent_id"]
        black_agent_id = game["black_agent_id"]
        white_agent_name = game["white_agent"]["name"]
        black_agent_name = game["black_agent"]["name"]
        move_count = len(state.get("move_history", []))
        result = game_status.get("result")
        reason = game_status.get("reason")
        game_json = json.dumps(game, ensure_ascii=False)

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO games (
                    game_id,
                    created_at,
                    updated_at,
                    white_agent_id,
                    black_agent_id,
                    white_agent_name,
                    black_agent_name,
                    move_count,
                    result,
                    reason,
                    game_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(game_id) DO UPDATE SET
                    updated_at=excluded.updated_at,
                    white_agent_id=excluded.white_agent_id,
                    black_agent_id=excluded.black_agent_id,
                    white_agent_name=excluded.white_agent_name,
                    black_agent_name=excluded.black_agent_name,
                    move_count=excluded.move_count,
                    result=excluded.result,
                    reason=excluded.reason,
                    game_json=excluded.game_json
                """,
                (
                    game_id,
                    created_at,
                    updated_at,
                    white_agent_id,
                    black_agent_id,
                    white_agent_name,
                    black_agent_name,
                    move_count,
                    result,
                    reason,
                    game_json,
                ),
            )
            conn.commit()

        return {
            "ok": True,
            "provider": "sqlite",
            "game_id": game_id,
            "move_count": move_count,
            "path": str(self.db_path),
        }

    def get_game(self, game_id: str) -> dict | None:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT game_json FROM games WHERE game_id = ?",
                (game_id,),
            )
            row = cursor.fetchone()

        if not row:
            return None

        return json.loads(row[0])

    def list_games(self, limit: int = 50) -> list[dict]:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                SELECT
                    game_id,
                    created_at,
                    updated_at,
                    white_agent_name,
                    black_agent_name,
                    move_count,
                    result,
                    reason
                FROM games
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()

        games = []

        for row in rows:
            games.append(
                {
                    "game_id": row[0],
                    "created_at": row[1],
                    "updated_at": row[2],
                    "white_agent_name": row[3],
                    "black_agent_name": row[4],
                    "move_count": row[5],
                    "result": row[6],
                    "reason": row[7],
                }
            )

        return games