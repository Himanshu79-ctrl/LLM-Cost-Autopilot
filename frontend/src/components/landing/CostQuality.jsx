function CostQuality() {
  return (
    <section className="section cost-section">
      <div className="cost-panel">
        <div className="cost-main">
          <span className="section-kicker">
            COST-AWARE INTELLIGENCE
          </span>

          <h2>
            Use expensive intelligence
            <br />
            <span>when it actually matters.</span>
          </h2>

          <p>
            RouteMind is designed around a simple idea: simple requests
            should not automatically consume your most expensive model.
          </p>
        </div>

        <div className="cost-readout">
          <div className="readout-row">
            <span>REQUEST</span>
            <strong>Explain REST API</strong>
          </div>

          <div className="readout-row">
            <span>COMPLEXITY</span>
            <strong className="green-text">LOW</strong>
          </div>

          <div className="readout-row">
            <span>ROUTE</span>
            <strong>LIGHTWEIGHT MODEL</strong>
          </div>

          <div className="readout-row">
            <span>STATUS</span>
            <strong className="green-text">
              VERIFIED
            </strong>
          </div>
        </div>
      </div>
    </section>
  );
}

export default CostQuality;