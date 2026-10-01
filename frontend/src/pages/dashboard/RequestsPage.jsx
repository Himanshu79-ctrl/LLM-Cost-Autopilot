import { useEffect, useState } from "react";
import { getRequestHistory } from "../../services/authService";
import DashboardHeader from "../../components/dashboard/DashboardHeader";
function RequestsPage() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRequests() {
      try {
        setLoading(true);
        setError("");

        const data = await getRequestHistory(50);

        setRequests(data);
      } catch (error) {
        setError(
          error.message || "Failed to load requests."
        );
      } finally {
        setLoading(false);
      }
    }

    loadRequests();
  }, []);

  return (
    <>
      <DashboardHeader />
    <section className="requests-page">
      <div className="requests-page-header">
        <div>
          <span className="page-kicker">
            REQUEST HISTORY
          </span>

          <h1>Your requests</h1>

          <p>
            Review your previous LLM routing requests.
          </p>
        </div>
      </div>

      <div className="requests-card">
        {loading ? (
          <div className="requests-empty">
            Loading requests...
          </div>
        ) : error ? (
          <div className="requests-empty requests-error">
            {error}
          </div>
        ) : requests.length === 0 ? (
          <div className="requests-empty">
            No requests yet.
          </div>
        ) : (
          <div className="requests-table-wrapper">
            <table className="requests-table">
              <thead>
                <tr>
                  <th>Request</th>
                  <th>Model</th>
                  <th>Provider</th>
                  <th>Complexity</th>
                  <th>Latency</th>
                  <th>Tokens</th>
                  <th>Cost</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {requests.map((request) => (
                  <tr key={request.id}>
                    <td>
                      <div className="request-table-prompt">
                        {request.prompt_preview ||
                          `Request #${request.id}`}
                      </div>

                      <span className="request-table-id">
                        #{request.id}
                      </span>
                    </td>

                    <td>
                      <span className="request-model">
                        {request.selected_model}
                      </span>
                    </td>

                    <td>
                      {request.selected_provider}
                    </td>

                    <td>
                      <span
                        className={`request-complexity request-complexity-${request.complexity_level}`}
                      >
                        {request.complexity_level}
                      </span>
                    </td>

                    <td>
                      {Math.round(request.latency_ms)} ms
                    </td>

                    <td>
                      {(
                        Number(request.input_tokens || 0) +
                        Number(request.output_tokens || 0)
                      ).toLocaleString()}
                    </td>

                    <td>
                      $
                      {Number(request.cost || 0).toFixed(
                        6
                      )}
                    </td>

                    <td>
                      {request.error_type ? (
                        <span className="request-status request-status-error">
                          Failed
                        </span>
                      ) : (
                        <span className="request-status request-status-success">
                          Completed
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
    </>
  );
}

export default RequestsPage;