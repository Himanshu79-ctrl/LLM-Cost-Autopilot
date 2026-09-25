import DashboardHeader from "../../components/dashboard/DashboardHeader";
import AskRouteMind from "../../components/dashboard/AskRouteMind";
import RoutingOverview from "../../components/dashboard/RoutingOverview";
import RecentRequests from "../../components/dashboard/RecentRequests";

function DashboardPage() {
  return (
    <>
      <DashboardHeader />

      <div className="dashboard-content">
        <AskRouteMind />

        <RoutingOverview />

        <RecentRequests />
      </div>
    </>
  );
}

export default DashboardPage;