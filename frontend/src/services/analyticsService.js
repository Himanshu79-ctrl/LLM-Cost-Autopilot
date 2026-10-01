import { getToken } from "./authService";

const API_BASE_URL = "http://localhost:8000";

async function request(endpoint) {
  const token = getToken();

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to fetch analytics data."
    );
  }

  return data;
}

export function getUsageSummary() {
  return request("/api/usage/summary");
}

export function getModelUsage() {
  return request("/api/usage/models");
}

export function getProviderUsage() {
  return request("/api/usage/providers");
}

export function getComplexityUsage() {
  return request("/api/usage/complexity");
}