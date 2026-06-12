import { axiosClient } from "./axiosClient";

export async function getSystemHealth() {
  const response = await axiosClient.get("/system/health");
  return response.data;
}

export async function getDbHealth() {
  const response = await axiosClient.get("/system/db-health");
  return response.data;
}

export async function getAgents() {
  const response = await axiosClient.get("/agents");
  return response.data;
}

export async function createGame(payload) {
  const response = await axiosClient.post("/game/new", payload);
  return response.data;
}

export async function playStep(gameId) {
  const response = await axiosClient.post(`/game/${gameId}/step`);
  return response.data;
}

export async function getHistory() {
  const response = await axiosClient.get("/history");
  return response.data;
}
