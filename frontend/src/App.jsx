import { useEffect, useState } from "react";
import "./index.css";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function App() {
  const [health, setHealth] = useState(null);
  const [dbHealth, setDbHealth] = useState(null);
  const [agents, setAgents] = useState([]);
  const [game, setGame] = useState(null);
  const [lastStep, setLastStep] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function apiGet(path) {
    const res = await fetch(`${API_BASE_URL}${path}`);
    if (!res.ok) throw new Error(`GET ${path} failed`);
    return res.json();
  }

  async function apiPost(path, body) {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) throw new Error(`POST ${path} failed`);
    return res.json();
  }

  async function loadStatus() {
    try {
      setError("");
      const healthData = await apiGet("/system/health");
      const dbData = await apiGet("/system/db-health");
      const agentsData = await apiGet("/agents");

      setHealth(healthData);
      setDbHealth(dbData);
      setAgents(agentsData.agents || []);
    } catch (err) {
      console.error(err);
      setError("Backend not connected. Start FastAPI first.");
    }
  }

  async function createMatch() {
    try {
      setLoading(true);
      setError("");

      const data = await apiPost("/game/new", {
        white_agent_id: "alpha_attacker",
        black_agent_id: "shadow_defender",
        max_moves: 120,
      });

      setGame(data.game);
      setLastStep(null);
    } catch (err) {
      console.error(err);
      setError("Could not create game.");
    } finally {
      setLoading(false);
    }
  }

  async function nextMove() {
    if (!game?.game_id) return;

    try {
      setLoading(true);
      setError("");

      const data = await apiPost(`/game/${game.game_id}/step`);
      setLastStep(data);
      setGame(data.game);
    } catch (err) {
      console.error(err);
      setError("Could not play next move.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadStatus();
  }, []);

  return (
    <div className="app">
      <header className="navbar">
        <div>
          <h1>Baymax</h1>
          <p>AI-vs-AI Chess Arena</p>
        </div>

        <div className="badge">Safe Frontend Shell</div>
      </header>

      {error && <div className="error">{error}</div>}

      <main className="grid">
        <section className="left">
          <div className="card hero">
            <span className="pill">Local-first · FastAPI · LangGraph · Stockfish · Ollama</span>

            <h2>Baymax AI Chess Arena</h2>

            <p>
              This is the stable frontend shell. It connects to the backend,
              creates AI matches, plays AI moves, and shows game state.
            </p>

            <div className="buttons">
              <button onClick={createMatch} disabled={loading}>
                Create AI Match
              </button>

              <button onClick={nextMove} disabled={loading || !game?.game_id}>
                Next AI Move
              </button>

              <button onClick={loadStatus} disabled={loading}>
                Refresh Status
              </button>
            </div>
          </div>

          <div className="stats">
            <div className="card">
              <h3>Backend</h3>
              <p>{health?.status === "ok" ? "Running" : "Not connected"}</p>
              <small>LLM: {health?.llm_model || "unknown"}</small>
            </div>

            <div className="card">
              <h3>SQLite</h3>
              <p>{dbHealth?.ok ? "Connected" : "Not connected"}</p>
              <small>Games: {dbHealth?.games_count ?? "—"}</small>
            </div>

            <div className="card">
              <h3>Agents</h3>
              <p>{agents.length} ready</p>
              <small>Alpha Attacker vs Shadow Defender</small>
            </div>
          </div>

          {game && (
            <div className="card">
              <h3>Current Match</h3>

              <div className="info">
                <p><b>Game ID:</b> {game.game_id}</p>
                <p><b>Turn:</b> {game.state.turn}</p>
                <p><b>White:</b> {game.white_agent.name}</p>
                <p><b>Black:</b> {game.black_agent.name}</p>
                <p><b>Moves:</b> {game.state.move_history.length}</p>
                <p><b>Status:</b> {game.state.game_status.reason}</p>
              </div>
            </div>
          )}

          {lastStep?.commentary && (
            <div className="card">
              <h3>Baymax Commentary</h3>
              <p>{lastStep.commentary.text}</p>
              <small>
                Provider: {lastStep.commentary.provider || "fallback"} · Model:{" "}
                {lastStep.commentary.model || "none"}
              </small>
            </div>
          )}
        </section>

        <section className="right">
          <div className="card">
            <h3>Board Placeholder</h3>

            <div className="board-placeholder">
              <div>Chess UI will be added next</div>
            </div>
          </div>

          <div className="card">
            <h3>Move History</h3>

            {game?.state?.move_history?.length ? (
              <div className="moves">
                {game.state.move_history.map((move, index) => (
                  <span key={`${move}-${index}`}>
                    {index + 1}. {move}
                  </span>
                ))}
              </div>
            ) : (
              <p className="muted">No moves yet.</p>
            )}
          </div>

          {game?.state?.fen && (
            <div className="card">
              <h3>Current FEN</h3>
              <code>{game.state.fen}</code>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
