import { createContext, useContext, useEffect, useState } from "react";

import {
  getCurrentUser,
  getToken,
  loginUser,
  registerUser,
  removeToken,
  saveToken,
} from "../services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function restoreSession() {
      const token = getToken();

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error("Failed to restore session:", error);

        removeToken();
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    restoreSession();
  }, []);

  async function login(credentials) {
    const data = await loginUser(credentials);

    saveToken(data.access_token);

    const currentUser = await getCurrentUser();

    setUser(currentUser);

    return currentUser;
  }

  async function register(userData) {
    return registerUser(userData);
  }

  function logout() {
    removeToken();
    setUser(null);
  }

  const value = {
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }

  return context;
}