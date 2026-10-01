import { useState } from "react";

import DashboardHeader from "../../components/dashboard/DashboardHeader";
import AskRouteMind from "../../components/dashboard/AskRouteMind";
import CurrentRequest from "../../components/dashboard/CurrentRequest";
import QuickStats from "../../components/dashboard/QuickStats";
import RecentRequests from "../../components/dashboard/RecentRequests";

function DashboardPage() {
  const [latestResponse, setLatestResponse] = useState(null);

  return (
    <>
      <DashboardHeader />

      <div className="dashboard-content">
        <div className="dashboard-layout">
          <main className="dashboard-main-column">
            <AskRouteMind onResponse={setLatestResponse} />
          </main>

          <aside className="dashboard-right-column">
            <CurrentRequest response={latestResponse} />

            <QuickStats />

            <RecentRequests
                currentRequestId={latestResponse?.request_id}
            />
          </aside>
        </div>
      </div>
    </>
  );
}

export default DashboardPage;