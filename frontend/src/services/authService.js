const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
//
async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const data = await response.json();

  if (!response.ok) {
    let message = "Something went wrong";

    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data.detail)) {
      message = data.detail
        .map((item) => item.msg || "Validation error")
        .join(", ");
    } else if (data.detail) {
      message = JSON.stringify(data.detail);
    }

    throw new Error(message);
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

export async function generateResponse(prompt) {
  const token = getToken();

  return request("/api/generate", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      prompt,
    }),
  });
}


export async function getRequestHistory(limit = 50) {
  const token = getToken();

  return request(`/api/usage/requests?limit=${limit}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}


export async function getUsageSummary() {
  const token = getToken();

  return request("/api/usage/summary", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function getProviderUsage() {
  const token = getToken();

  return request("/api/usage/providers", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function getModelUsage() {
  const token = getToken();

  return request("/api/usage/models", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export async function getComplexityUsage() {
  const token = getToken();

  return request("/api/usage/complexity", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}