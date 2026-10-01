import { Outlet } from "react-router-dom";
import DashboardRail from "../components/dashboard/DashboardRail";
import "../styles/dashboard.css";

function DashboardLayout() {
  return (
    <main className="dashboard">
      <DashboardRail />

      <div className="dashboard-main">
        <Outlet />
      </div>
    </main>
  );
}

export default DashboardLayout;