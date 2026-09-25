import { Link, useLocation } from "react-router-dom";

const navigation = [
  {
    label: "Ask",
    path: "/dashboard",
  },
  {
    label: "Analytics",
    path: "/dashboard/analytics",
  },
  {
    label: "Requests",
    path: "/dashboard/requests",
  },
];

function DashboardRail() {
  const location = useLocation();

  return (
    <aside className="dashboard-rail">
      <Link
        to="/dashboard"
        className="rail-logo"
        aria-label="RouteMind dashboard"
      >
        <span className="rail-logo-mark" />
      </Link>

      <nav className="rail-navigation" aria-label="Dashboard navigation">
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
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

export default DashboardRail;