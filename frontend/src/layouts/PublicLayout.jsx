import { Outlet } from "react-router-dom";
import Navbar from "../components/common/Navbar";

function PublicLayout() {
  return (
    <div className="public-layout">
      <Navbar />

      <Outlet />
    </div>
  );
}

export default PublicLayout;