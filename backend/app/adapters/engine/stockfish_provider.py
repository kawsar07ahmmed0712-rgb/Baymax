from pathlib import Path

import chess
import chess.engine

from app.adapters.engine.base import BaseChessEngine
from app.core.config import settings


class StockfishProvider(BaseChessEngine):
    """
    Stockfish UCI engine provider.
    """

    def __init__(self, engine_path: str | None = None):
        self.engine_path = self._resolve_engine_path(
            engine_path or settings.stockfish_path
        )

    def _resolve_engine_path(self, raw_path: str) -> Path:
        """
        Resolve Stockfish path safely from different working directories.
        """
        path = Path(raw_path)

        if path.is_absolute() and path.exists():
            return path

        current_working_dir_candidate = Path.cwd() / path

        # file path:
        # backend/app/adapters/engine/stockfish_provider.py
        backend_root = Path(__file__).resolve().parents[3]
        project_root = Path(__file__).resolve().parents[4]

        candidates = [
            current_working_dir_candidate,
            backend_root / path,
            project_root / path,
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        raise FileNotFoundError(
            "Stockfish executable not found. Expected one of these paths:\n"
            + "\n".join(str(candidate) for candidate in candidates)
            + "\n\nPlace Stockfish here: Baymax/backend/stockfish/stockfish.exe"
        )

    def _create_board(self, fen: str) -> chess.Board:
        try:
            return chess.Board(fen)
        except ValueError as exc:
            raise ValueError(f"Invalid FEN: {fen}") from exc

    def health_check(self) -> dict:
        """
        Check whether Stockfish can start.
        """
        with chess.engine.SimpleEngine.popen_uci(str(self.engine_path)) as engine:
            return {
                "status": "ok",
                "engine": "stockfish",
                "path": str(self.engine_path),
                "id": engine.id,
            }

    def get_best_move(self, fen: str, depth: int | None = None) -> dict:
        """
        Get best move from Stockfish.
        """
        board = self._create_board(fen)
        search_depth = depth or settings.stockfish_depth

        if board.is_game_over(claim_draw=True):
            return {
                "ok": False,
                "reason": "Game is already over",
                "best_move": None,
                "fen": fen,
            }

        with chess.engine.SimpleEngine.popen_uci(str(self.engine_path)) as engine:
            result = engine.play(
                board,
                chess.engine.Limit(depth=search_depth),
            )

        if result.move is None:
            return {
                "ok": False,
                "reason": "Stockfish did not return a move",
                "best_move": None,
                "fen": fen,
            }

        return {
            "ok": True,
            "engine": "stockfish",
            "depth": search_depth,
            "fen": fen,
            "best_move": result.move.uci(),
            "ponder": result.ponder.uci() if result.ponder else None,
        }

    def get_top_moves(self, fen: str, depth: int | None = None, top_k: int | None = None) -> list[dict]:
        """
        Get top candidate moves from Stockfish using MultiPV analysis.
        """
        board = self._create_board(fen)
        search_depth = depth or settings.stockfish_depth
        candidate_count = top_k or settings.stockfish_top_k

        if board.is_game_over(claim_draw=True):
            return []

        with chess.engine.SimpleEngine.popen_uci(str(self.engine_path)) as engine:
            info_list = engine.analyse(
                board,
                chess.engine.Limit(depth=search_depth),
                multipv=candidate_count,
            )

        candidates = []

        for item in info_list:
            pv = item.get("pv", [])
            score = item.get("score")

            if not pv:
                continue

            move = pv[0]

            candidates.append(
                {
                    "move": move.uci(),
                    "san": board.san(move),
                    "score": str(score) if score else None,
                    "depth": item.get("depth"),
                }
            )

        return candidates