import { useEffect, useState } from "react";
import { Activity, Database, Play, ShieldCheck } from "lucide-react";

import {
  createGame,
  getAgents,
  getDbHealth,
  getSystemHealth,
  playStep,
} from "../api/gameApi";

import Button from "../components/common/Button";
import Card from "../components/common/Card";
import ChessPreview from "../components/chess/ChessPreview";

export default function Home() {
  const [health, setHealth] = useState(null);
  const [dbHealth, setDbHealth] = useState(null);
  const [agents, setAgents] = useState([]);
  const [game, setGame] = useState(null);
  const [lastStep, setLastStep] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  async function loadInitialData() {
    try {
      setApiError("");

      const [healthData, dbData, agentsData] = await Promise.all([
        getSystemHealth(),
        getDbHealth(),
        getAgents(),
      ]);

      setHealth(healthData);
      setDbHealth(dbData);
      setAgents(agentsData.agents || []);
    } catch (error) {
      console.error(error);
      setApiError("Backend not connected. Start FastAPI server first.");
    }
  }

  async function handleCreateGame() {
    setLoading(true);

    try {
      setApiError("");

      const data = await createGame({
        white_agent_id: "alpha_attacker",
        black_agent_id: "shadow_defender",
        max_moves: 120,
      });

      setGame(data.game);
      setLastStep(null);
    } catch (error) {
      console.error(error);
      setApiError("Could not create game. Check backend, Stockfish, and database.");
    } finally {
      setLoading(false);
    }
  }

  async function handleNextMove() {
    if (!game?.game_id) return;

    setLoading(true);

    try {
      setApiError("");

      const data = await playStep(game.game_id);

      setLastStep(data);
      setGame(data.game);
    } catch (error) {
      console.error(error);
      setApiError("Could not play move. Check backend, Stockfish, and Ollama.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadInitialData();
  }, []);

  const fen = game?.state?.fen;
  const moveHistory = game?.state?.move_history || [];

  return (
    <main className="mx-auto max-w-7xl px-5 py-8">
      {apiError && (
        <div className="mb-5 rounded-2xl border border-rose-500/40 bg-rose-500/10 p-4 text-sm text-rose-200">
          {apiError}
        </div>
      )}

      <section className="grid gap-6 lg:grid-cols-[1fr_560px]">
        <div className="space-y-6">
          <Card className="p-7">
            <div className="mb-4 inline-flex rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-300">
              Local-first · LangGraph · Stockfish · Ollama
            </div>

            <h2 className="text-4xl font-black tracking-tight text-white sm:text-5xl">
              Baymax AI Chess Arena
            </h2>

            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
              A deploy-ready AI-vs-AI chess platform where LangGraph controls the
              agent workflow, Stockfish calculates moves, python-chess validates
              rules, SQLite saves games, and Ollama explains each move locally.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Button onClick={handleCreateGame} disabled={loading}>
                <span className="inline-flex items-center gap-2">
                  <Play size={16} />
                  Create AI Match
                </span>
              </Button>

              <Button
                variant="secondary"
                onClick={handleNextMove}
                disabled={loading || !game?.game_id}
              >
                Next AI Move
              </Button>

              <Button variant="secondary" onClick={loadInitialData} disabled={loading}>
                Refresh Status
              </Button>
            </div>
          </Card>

          <div className="grid gap-4 sm:grid-cols-3">
            <Card className="p-5">
              <div className="flex items-center gap-2 text-blue-300">
                <Activity size={18} />
                <span className="text-sm font-bold">Backend</span>
              </div>
              <p className="mt-3 text-sm text-slate-300">
                {health?.status === "ok" ? "Running" : "Not connected"}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                LLM: {health?.llm_model || "unknown"}
              </p>
            </Card>

            <Card className="p-5">
              <div className="flex items-center gap-2 text-emerald-300">
                <Database size={18} />
                <span className="text-sm font-bold">SQLite</span>
              </div>
              <p className="mt-3 text-sm text-slate-300">
                {dbHealth?.ok ? "Connected" : "Not connected"}
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Games: {dbHealth?.games_count ?? "—"}
              </p>
            </Card>

            <Card className="p-5">
              <div className="flex items-center gap-2 text-purple-300">
                <ShieldCheck size={18} />
                <span className="text-sm font-bold">Agents</span>
              </div>
              <p className="mt-3 text-sm text-slate-300">
                {agents.length} ready
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Alpha vs Shadow
              </p>
            </Card>
          </div>

          {game && (
            <Card className="p-5">
              <h3 className="mb-3 text-lg font-bold text-white">Current Match</h3>

              <div className="grid gap-3 text-sm text-slate-300 sm:grid-cols-2">
                <p><span className="text-slate-500">Game ID:</span> {game.game_id}</p>
                <p><span className="text-slate-500">Turn:</span> {game.state.turn}</p>
                <p><span className="text-slate-500">White:</span> {game.white_agent.name}</p>
                <p><span className="text-slate-500">Black:</span> {game.black_agent.name}</p>
                <p><span className="text-slate-500">Moves:</span> {moveHistory.length}</p>
                <p><span className="text-slate-500">Status:</span> {game.state.game_status.reason}</p>
              </div>
            </Card>
          )}

          {lastStep?.commentary && (
            <Card className="p-5">
              <h3 className="mb-2 text-lg font-bold text-white">Baymax Commentary</h3>

              <p className="text-sm leading-6 text-slate-300">
                {lastStep.commentary.text}
              </p>

              <p className="mt-2 text-xs text-slate-500">
                Provider: {lastStep.commentary.provider || "fallback"} · Model:{" "}
                {lastStep.commentary.model || "none"}
              </p>
            </Card>
          )}
        </div>

        <div className="space-y-4">
          <ChessPreview fen={fen} />

          <Card className="p-5">
            <h3 className="mb-3 text-lg font-bold text-white">Move History</h3>

            <div className="max-h-56 overflow-auto rounded-xl bg-slate-950 p-4 text-sm text-slate-300">
              {moveHistory.length ? (
                <div className="flex flex-wrap gap-2">
                  {moveHistory.map((move, index) => (
                    <span
                      key={`${move}-${index}`}
                      className="rounded-lg bg-slate-800 px-2 py-1"
                    >
                      {index + 1}. {move}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-slate-500">
                  No moves yet. Create a match and click Next AI Move.
                </p>
              )}
            </div>
          </Card>
        </div>
      </section>
    </main>
  );
}
