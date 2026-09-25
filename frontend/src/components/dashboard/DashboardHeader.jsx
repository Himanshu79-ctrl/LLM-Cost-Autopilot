import { useAuth } from "../../context/AuthContext";

function DashboardHeader() {
  const { user, logout } = useAuth();

  return (
    <header className="dashboard-topbar">
      <h1>Ask RouteMind</h1>

      <div className="dashboard-user">
        <span>{user?.name}</span>

        <button
          type="button"
          onClick={logout}
          className="dashboard-logout"
        >
          Log out
        </button>
      </div>
    </header>
  );
}

export default DashboardHeader;