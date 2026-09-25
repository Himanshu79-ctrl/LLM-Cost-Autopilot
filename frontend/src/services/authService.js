const API_BASE_URL = "http://localhost:8000";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || data.message || "Something went wrong",
    );
  }

  return data;
}

export async function registerUser(userData) {
  return request("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(userData),
  });
}

export async function loginUser(credentials) {
  return request("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export async function getCurrentUser() {
  const token = getToken();

  return request("/api/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function saveToken(token) {
  localStorage.setItem("routemind_token", token);
}

export function getToken() {
  return localStorage.getItem("routemind_token");
}

export function removeToken() {
  localStorage.removeItem("routemind_token");
}

export function isAuthenticated() {
  return Boolean(getToken());
}