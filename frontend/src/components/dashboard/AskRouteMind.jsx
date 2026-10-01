import { useState } from "react";
import { generateResponse } from "../../services/authService";

const examples = [
  "How does Redis work?",
  "What is PostgreSQL?",
  "Explain Django ORM",
  "Compare React vs Next.js",
];

function AskRouteMind({ onResponse }) {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmedPrompt = prompt.trim();

    if (!trimmedPrompt || loading) {
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await generateResponse(trimmedPrompt);

      const result = {
        ...data,
        prompt: trimmedPrompt,
        createdAt: new Date(),
      };

      setResponse(result);
      onResponse(result);
    } catch (error) {
      setError(
        error.message || "Failed to generate response."
      );
    } finally {
      setLoading(false);
    }
  }

  function selectExample(example) {
    setPrompt(example);
  }

  return (
    <section className="ask-section">
      <div className="ask-heading">
        <span className="ask-kicker">
          ASK ROUTEMIND
        </span>

        <h1>
          What do you want
          <br />
          to <span>solve?</span>
        </h1>

        <p>
          Describe your problem in natural language.
          RouteMind will find the right model for the task.
        </p>
      </div>

      <form
        className="prompt-composer"
        onSubmit={handleSubmit}
      >
        <textarea
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Ask a question, explain a problem, write code..."
          disabled={loading}
        />

        <div className="composer-footer">
          <div className="composer-context">
            <span className="composer-icon">⌕</span>
            <span>Add context <small>(optional)</small></span>
          </div>

          <div className="composer-actions">
            <span className="character-count">
              {prompt.length}/2000
            </span>

            <button
              type="submit"
              className="send-button"
              disabled={!prompt.trim() || loading}
            >
              {loading ? "Routing..." : "Send"}
              {!loading && <span>→</span>}
            </button>
          </div>
        </div>
      </form>

      <div className="example-row">
        <span className="example-label">
          <span>✧</span>
          Try these examples:
        </span>

        <div className="example-buttons">
          {examples.map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => selectExample(example)}
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="dashboard-error">
          {error}
        </div>
      )}

      {response && (
        <article className="conversation-card">
          <div className="conversation-header">
            <div className="conversation-author">
              <span className="ai-avatar">R</span>

              <div>
                <strong>RouteMind</strong>
                <span>
                  · Just now
                </span>
              </div>
            </div>

            <span className="conversation-model">
              {response.model}
            </span>
          </div>

          <div className="conversation-body">
            {response.output}
          </div>

          <div className="conversation-actions">
            <button type="button">
              Copy
            </button>

            <button type="button" aria-label="Good response">
              ♡
            </button>

            <button type="button" aria-label="Bad response">
              ♧
            </button>

            <button type="button">
              ↻ Regenerate
            </button>
          </div>
        </article>
      )}
    </section>
  );
}

export default AskRouteMind;