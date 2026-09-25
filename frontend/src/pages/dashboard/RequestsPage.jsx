function RequestsPage() {
  return (
        <div className="requests-page">
          <header className="page-heading">
            <div>
              <span className="dashboard-section-kicker">
                03 / REQUESTS
              </span>

              <h1>Request history</h1>

              <p>
                Review every request processed through the
                RouteMind routing engine.
              </p>
            </div>
          </header>

          <section className="requests-panel">
            <div className="request-row request-row-header">
              <span>REQUEST</span>
              <span>MODEL</span>
              <span>COMPLEXITY</span>
              <span>LATENCY</span>
              <span>COST</span>
              <span>STATUS</span>
            </div>

            <div className="request-empty">
              <span className="request-empty-mark">
                —
              </span>

              <p>No requests yet.</p>

              <span>
                Routed requests will appear here.
              </span>
            </div>
          </section>
        </div>
  );
}

export default RequestsPage;