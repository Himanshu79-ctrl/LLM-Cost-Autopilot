import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import PublicLayout from "../layouts/PublicLayout";

import LandingPage from "../pages/public/LandingPage";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

import ProtectedRoute from "./ProtectedRoute";

import DashboardLayout from "../layouts/DashboardLayout";

import DashboardPage from "../pages/dashboard/DashboardPage";
import AnalyticsPage from "../pages/dashboard/AnalyticsPage";
import RequestsPage from "../pages/dashboard/RequestsPage";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public pages */}
        <Route element={<PublicLayout />}>
          <Route
            path="/"
            element={<LandingPage />}
          />
        </Route>

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        {/* Protected application */}
        <Route element={<ProtectedRoute />}>
          <Route element={<DashboardLayout />}>

            <Route
              path="/dashboard"
              element={<DashboardPage />}
            />

            <Route
              path="/dashboard/analytics"
              element={<AnalyticsPage />}
            />

            <Route
              path="/dashboard/requests"
              element={<RequestsPage />}
            />

          </Route>
        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;