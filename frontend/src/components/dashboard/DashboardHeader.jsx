import { useAuth } from "../../context/AuthContext";

function DashboardHeader() {
  const { user, logout } = useAuth();

  const initial =
    user?.name?.charAt(0)?.toUpperCase() || "U";

  return (
    <header className="dashboard-topbar">
      <div className="topbar-actions">
        <button
          type="button"
          className="theme-button"
          aria-label="Toggle theme"
        >
          ☾
        </button>

        <div className="topbar-divider" />

        <div className="dashboard-user">
          <span className="dashboard-user-avatar">
            {initial}
          </span>

          <span className="dashboard-user-name">
            {user?.name || "User"}
          </span>

          <button
            type="button"
            className="dashboard-user-menu"
            aria-label="User menu"
          >
           ⌄
          </button>
        </div>

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