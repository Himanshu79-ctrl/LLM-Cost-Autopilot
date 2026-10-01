import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getRequestHistory } from "../../services/authService";

function RecentRequests({ currentRequestId }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadRequests() {
    try {
      setError("");

      const data = await getRequestHistory(6);

      setRequests(data);
    } catch (error) {
      setError(
        error.message || "Failed to load recent requests."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadRequests();
  }, [currentRequestId]);

  const recentRequests = requests
    .filter((request) => request.id !== currentRequestId)
    .slice(0, 5);

  return (
    <section className="side-card recent-card">
      <div className="side-card-header">
        <div className="side-title-group">
          <span className="side-icon recent-icon">
            ◷
          </span>

          <h2>Recent requests</h2>
        </div>

        <Link
          to="/dashboard/requests"
          className="view-all-button"
        >
          View all →
        </Link>
      </div>

      {loading ? (
        <div className="side-empty recent-empty">
          Loading recent requests...
        </div>
      ) : error ? (
        <div className="side-empty recent-empty">
          {error}
        </div>
      ) : recentRequests.length === 0 ? (
        <div className="side-empty recent-empty">
          Your routed requests will appear here.
        </div>
      ) : (
        <div className="recent-request-list">
          {recentRequests.map((request) => (
            <div
              key={request.id}
              className="recent-request-item"
            >
              <div className="recent-request-main">
                <strong className="recent-request-prompt">
                  {request.prompt_preview ||
                    `Request #${request.id}`}
                </strong>

                <span className="recent-request-meta">
                  {request.selected_model}
                </span>
              </div>

              <div className="recent-request-side">
                <span
                  className={`recent-complexity recent-complexity-${request.complexity_level}`}
                >
                  {request.complexity_level}
                </span>

                <span className="recent-request-cost">
                  ${Number(request.cost).toFixed(6)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default RecentRequests;