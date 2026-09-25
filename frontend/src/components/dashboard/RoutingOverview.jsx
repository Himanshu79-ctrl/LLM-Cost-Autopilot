const metrics = [
  {
    label: "COMPLEXITY",
    value: "—",
    status: "WAITING",
  },
  {
    label: "MODEL",
    value: "—",
    status: "NOT ROUTED",
  },
  {
    label: "LATENCY",
    value: "—",
    status: "NO REQUEST",
  },
  {
    label: "COST",
    value: "—",
    status: "NO REQUEST",
  },
];

function RoutingOverview() {
  return (
    <section className="routing-overview">
      <div className="dashboard-section-header">
        <div>
          <span className="dashboard-section-kicker">
            ROUTING
          </span>

          <h2>Request intelligence</h2>
        </div>

        <span className="dashboard-section-meta">
          LAST REQUEST
        </span>
      </div>

      <div className="metrics-grid">
        {metrics.map((metric) => (
          <article
            className="metric-card"
            key={metric.label}
          >
            <span className="metric-label">
              {metric.label}
            </span>

            <strong className="metric-value">
              {metric.value}
            </strong>

            <span className="metric-status">
              {metric.status}
            </span>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RoutingOverview;