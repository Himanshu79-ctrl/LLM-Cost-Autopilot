import { useState } from "react";

function AskRouteMind() {
  const [prompt, setPrompt] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    if (!prompt.trim()) {
      return;
    }

    console.log("Prompt:", prompt);
  }

  return (
    <section className="ask-panel">
      <div className="ask-panel-header">
        <div>
          <span className="panel-kicker">
            ASK ROUTEMIND
          </span>

          <h2>
            What do you want
            <br />
            to solve?
          </h2>
        </div>
      </div>

      <form
        className="ask-form"
        onSubmit={handleSubmit}
      >
        <textarea
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Ask a question, explain a problem, write code, analyze something..."
          rows={7}
        />

        <div className="ask-form-footer">
          <span className="ask-hint">
            RouteMind will analyze complexity and select
            the appropriate model.
          </span>

          <button
            type="submit"
            className="route-button"
            disabled={!prompt.trim()}
          >
            Route <span>→</span>
          </button>
        </div>
      </form>

      <div className="ask-example">
        <span>Try:</span>

        <button
          type="button"
          onClick={() =>
            setPrompt(
              "Explain how a distributed cache works and when I should use one."
            )
          }
        >
          Explain how a distributed cache works and when I should use one.
        </button>
      </div>
    </section>
  );
}

export default AskRouteMind;