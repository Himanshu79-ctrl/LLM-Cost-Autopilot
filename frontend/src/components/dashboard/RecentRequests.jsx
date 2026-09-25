function RecentRequests() {
  return (
    <section className="recent-requests">
      <div className="dashboard-section-header">
        <div>
          <span className="dashboard-section-kicker">
            REQUEST LOG
          </span>

          <h2>Recent requests</h2>
        </div>

        <span className="dashboard-section-meta">
          0 REQUESTS
        </span>
      </div>

      <div className="request-table">
        <div className="request-row request-row-header">
          <span>REQUEST</span>
          <span>MODEL</span>
          <span>COMPLEXITY</span>
          <span>COST</span>
          <span>STATUS</span>
        </div>

        <div className="request-empty">
          <span className="request-empty-mark">—</span>

          <p>
            No requests yet.
          </p>

          <span>
            Your routed requests will appear here.
          </span>
        </div>
      </div>
    </section>
  );
}

export default RecentRequests;