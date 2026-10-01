function CurrentRequest({ response }) {
  return (
    <section className="side-card current-request-card">
      <div className="side-card-header">
        <div className="side-title-group">
          <span className="side-icon request-icon">
            ✦
          </span>

          <h2>Current Request</h2>
        </div>

        {response && (
          <span className="completed-badge">
            Completed
          </span>
        )}
      </div>

      {!response ? (
        <div className="side-empty">
          Send a prompt to see how RouteMind handled
          your request.
        </div>
      ) : (
        <div className="request-details">
          <div className="request-detail">
            <span>Topic</span>
            <strong>{response.prompt}</strong>
          </div>

          <div className="request-detail">
            <span>Model</span>
            <strong>{response.model}</strong>
          </div>

          <div className="request-detail">
            <span>Complexity</span>
            <strong>
              {response.complexity?.toUpperCase()}
            </strong>
          </div>

          <div className="request-detail">
            <span>Latency</span>
            <strong>
              {Math.round(response.latency_ms)} ms
            </strong>
          </div>

          <div className="request-detail">
            <span>Cost</span>
            <strong>
              ${Number(response.cost).toFixed(8)}
            </strong>
          </div>
        </div>
      )}
    </section>
  );
}

export default CurrentRequest;