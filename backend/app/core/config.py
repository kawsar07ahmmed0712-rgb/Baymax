import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "Baymax")
    app_env: str = os.getenv("APP_ENV", "local")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    chess_engine_provider: str = os.getenv("CHESS_ENGINE_PROVIDER", "stockfish")
    stockfish_path: str = os.getenv("STOCKFISH_PATH", "backend/stockfish/stockfish.exe")
    stockfish_depth: int = int(os.getenv("STOCKFISH_DEPTH", "8"))
    stockfish_top_k: int = int(os.getenv("STOCKFISH_TOP_K", "5"))

    database_provider: str = os.getenv("DATABASE_PROVIDER", "sqlite")
    sqlite_path: str = os.getenv("SQLITE_PATH", "backend/app/storage/baymax.db")

    memory_provider: str = os.getenv("MEMORY_PROVIDER", "sqlite")

    auto_play_delay_ms: int = int(os.getenv("AUTO_PLAY_DELAY_MS", "1000"))
    max_game_moves: int = int(os.getenv("MAX_GAME_MOVES", "300"))


settings = Settings()