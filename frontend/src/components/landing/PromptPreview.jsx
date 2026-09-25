import RoutingFlow from "./RoutingFlow";

function PromptPreview() {
  return (
    <section className="prompt-preview" id="product">
      <div className="prompt-header">
        <div className="prompt-status">
          <span className="status-dot" />
          ROUTEMIND READY
        </div>

        <span className="prompt-meta">
          INTELLIGENT ROUTING
        </span>
      </div>

      <div className="prompt-body">
        <div className="prompt-copy">
          <span className="prompt-label">
            ASK ROUTEMIND
          </span>

          <p>
            What do you want to solve?
          </p>

          <span className="prompt-example">
            Explain how a distributed cache works...
          </span>
        </div>

        <button
          type="button"
          className="prompt-arrow"
          aria-label="Try RouteMind"
        >
          →
        </button>
      </div>

      <RoutingFlow />
    </section>
  );
}

export default PromptPreview;