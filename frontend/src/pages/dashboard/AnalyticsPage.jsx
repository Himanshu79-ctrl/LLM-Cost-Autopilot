const analytics = [
  {
    label: "TOTAL REQUESTS",
    value: "—",
    detail: "No requests yet",
  },
  {
    label: "TOTAL COST",
    value: "—",
    detail: "Awaiting usage",
  },
  {
    label: "AVG LATENCY",
    value: "—",
    detail: "Awaiting usage",
  },
  {
    label: "AVG QUALITY",
    value: "—",
    detail: "Awaiting verification",
  },
];

const modelUsage = [
  {
    model: "LIGHTWEIGHT",
    requests: "—",
    percentage: "—",
  },
  {
    model: "BALANCED",
    requests: "—",
    percentage: "—",
  },
  {
    model: "POWERFUL",
    requests: "—",
    percentage: "—",
  },
];

function AnalyticsPage() {
  return (
        <div className="analytics-page">
          <header className="page-heading">
            <div>
              <span className="dashboard-section-kicker">
                02 / ANALYTICS
              </span>

              <h1>Usage intelligence</h1>

              <p>
                Understand how RouteMind is routing your requests,
                consuming tokens, and managing cost.
              </p>
            </div>
          </header>

          <section className="analytics-metrics">
            {analytics.map((item) => (
              <article
                className="analytics-metric"
                key={item.label}
              >
                <span>{item.label}</span>

                <strong>{item.value}</strong>

                <small>{item.detail}</small>
              </article>
            ))}
          </section>

          <section className="analytics-panel">
            <div className="dashboard-section-header">
              <div>
                <span className="dashboard-section-kicker">
                  MODEL DISTRIBUTION
                </span>

                <h2>Routing usage</h2>
              </div>
            </div>

            <div className="model-usage-list">
              {modelUsage.map((item) => (
                <div
                  className="model-usage-row"
                  key={item.model}
                >
                  <span>{item.model}</span>

                  <div className="model-usage-bar">
                    <span />
                  </div>

                  <span>{item.requests}</span>
                  <span>{item.percentage}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="analytics-panel">
            <div className="dashboard-section-header">
              <div>
                <span className="dashboard-section-kicker">
                  PERFORMANCE
                </span>

                <h2>Cost vs quality</h2>
              </div>
            </div>

            <div className="analytics-empty-chart">
              <span>NO DATA</span>

              <p>
                Performance data will appear after your first
                routed request.
              </p>
            </div>
          </section>
        </div>
  );
}

export default AnalyticsPage;