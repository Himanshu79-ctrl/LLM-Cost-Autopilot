import { Outlet } from "react-router-dom";

import DashboardRail from "../components/dashboard/DashboardRail";

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