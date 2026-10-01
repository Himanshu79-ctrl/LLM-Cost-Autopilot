import { Link, useLocation } from "react-router-dom";

const navigation = [
  {
    label: "Ask",
    path: "/dashboard",
    icon: "✦",
  },
  {
    label: "Analytics",
    path: "/dashboard/analytics",
    icon: "▥",
  },
  {
    label: "Requests",
    path: "/dashboard/requests",
    icon: "◷",
  },
];

function DashboardRail() {
  const location = useLocation();

  return (
    <aside className="dashboard-rail">
      <Link to="/dashboard" className="rail-brand">
        <span className="rail-brand-mark">
          <span />
        </span>

        <span className="rail-brand-name">
          RouteMind
        </span>
      </Link>

      <nav className="rail-navigation">
        {navigation.map((item) => {
          const isActive =
            item.path === "/dashboard"
              ? location.pathname === "/dashboard"
              : location.pathname.startsWith(item.path);

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`rail-item ${
                isActive ? "rail-item-active" : ""
              }`}
            >
              <span className="rail-item-icon">
                {item.icon}
              </span>

              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="rail-status">
        <div className="rail-status-row">
          <span className="rail-status-dot" />
          <span>System Online</span>
        </div>

        <span className="rail-status-text">
          Ready to help
        </span>
      </div>
    </aside>
  );
}

export default DashboardRail;