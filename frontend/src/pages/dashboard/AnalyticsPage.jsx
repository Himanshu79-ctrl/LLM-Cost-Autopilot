import { useEffect, useState } from "react";

import {
  getUsageSummary,
  getModelUsage,
  getProviderUsage,
  getComplexityUsage,
} from "../../services/analyticsService";


function formatCost(value) {
  return `$${Number(value || 0).toFixed(6)}`;
}


function formatNumber(value) {
  return Number(value || 0).toLocaleString();
}


function AnalyticsPage() {
  const [summary, setSummary] = useState(null);
  const [models, setModels] = useState([]);
  const [providers, setProviders] = useState([]);
  const [complexity, setComplexity] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    async function loadAnalytics() {
      try {
        setLoading(true);
        setError("");

        const [
          summaryData,
          modelData,
          providerData,
          complexityData,
        ] = await Promise.all([
          getUsageSummary(),
          getModelUsage(),
          getProviderUsage(),
          getComplexityUsage(),
        ]);

        setSummary(summaryData);
        setModels(modelData);
        setProviders(providerData);
        setComplexity(complexityData);
      } catch (err) {
        setError(
          err.message || "Failed to load analytics."
        );
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);


  if (loading) {
    return (
      <div className="analytics-page">
        <div className="analytics-loading">
          Loading usage intelligence...
        </div>
      </div>
    );
  }


  if (error) {
    return (
      <div className="analytics-page">
        <div className="analytics-error">
          {error}
        </div>
      </div>
    );
  }


  const totalModelRequests = models.reduce(
    (total, item) => total + Number(item.requests || 0),
    0
  );

  const totalProviderRequests = providers.reduce(
    (total, item) => total + Number(item.requests || 0),
    0
  );

  const totalComplexityRequests = complexity.reduce(
    (total, item) => total + Number(item.requests || 0),
    0
  );


  return (
    <div className="analytics-page">

      {/* PAGE HEADER */}

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


      {/* TOP METRICS */}

      <section className="analytics-metrics">

        <article className="analytics-metric">
          <span>TOTAL REQUESTS</span>

          <strong>
            {formatNumber(summary?.total_requests)}
          </strong>

          <small>
            Routed requests
          </small>
        </article>


        <article className="analytics-metric">
          <span>TOTAL COST</span>

          <strong>
            {formatCost(summary?.total_cost)}
          </strong>

          <small>
            Estimated LLM spend
          </small>
        </article>


        <article className="analytics-metric">
          <span>AVG LATENCY</span>

          <strong>
            {Math.round(
              Number(summary?.average_latency_ms || 0)
            )}
            <em> ms</em>
          </strong>

          <small>
            Average generation latency
          </small>
        </article>


        <article className="analytics-metric">
          <span>AVG QUALITY</span>

          <strong>
            {summary?.average_quality_score
              ? Number(
                  summary.average_quality_score
                ).toFixed(1)
              : "—"}
          </strong>

          <small>
            Verified responses
          </small>
        </article>

      </section>


      {/* MODEL DISTRIBUTION */}

      <section className="analytics-panel">

        <div className="dashboard-section-header">
          <div>
            <span className="dashboard-section-kicker">
              MODEL DISTRIBUTION
            </span>

            <h2>Routing usage</h2>
          </div>

          <span className="analytics-panel-meta">
            {formatNumber(totalModelRequests)} requests
          </span>
        </div>


        {models.length === 0 ? (
          <div className="analytics-empty-chart">
            <span>NO MODEL DATA</span>
            <p>
              Model usage will appear after your first
              routed request.
            </p>
          </div>
        ) : (
          <div className="model-usage-list">

            {models.map((item) => {

              const percentage =
                totalModelRequests > 0
                  ? (
                      (Number(item.requests) /
                        totalModelRequests) *
                      100
                    )
                  : 0;

              return (
                <div
                  className="model-usage-row"
                  key={item.model}
                >

                  <span title={item.model}>
                    {item.model}
                  </span>

                  <div className="model-usage-bar">
                    <span
                      style={{
                        width: `${percentage}%`,
                      }}
                    />
                  </div>

                  <span>
                    {formatNumber(item.requests)}
                  </span>

                  <span>
                    {percentage.toFixed(1)}%
                  </span>

                </div>
              );
            })}

          </div>
        )}

      </section>


      {/* PROVIDER + COMPLEXITY */}

      <div className="analytics-two-column">

        {/* PROVIDERS */}

        <section className="analytics-panel">

          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-kicker">
                PROVIDERS
              </span>

              <h2>Provider usage</h2>
            </div>
          </div>


          {providers.length === 0 ? (
            <div className="analytics-empty-chart">
              <span>NO PROVIDER DATA</span>
            </div>
          ) : (
            <div className="provider-usage-list">

              {providers.map((item) => {

                const percentage =
                  totalProviderRequests > 0
                    ? (
                        (Number(item.requests) /
                          totalProviderRequests) *
                        100
                      )
                    : 0;

                return (
                  <div
                    className="provider-usage-row"
                    key={item.provider}
                  >

                    <div>
                      <strong>
                        {item.provider}
                      </strong>

                      <span>
                        {formatNumber(item.requests)}
                        {" "}requests · {percentage.toFixed(1)}%
                      </span>
                    </div>

                    <strong>
                      {formatCost(item.cost)}
                    </strong>

                  </div>
                );
              })}

            </div>
          )}

        </section>


        {/* COMPLEXITY */}

        <section className="analytics-panel">

          <div className="dashboard-section-header">
            <div>
              <span className="dashboard-section-kicker">
                COMPLEXITY
              </span>

              <h2>Request distribution</h2>
            </div>
          </div>


          {complexity.length === 0 ? (
            <div className="analytics-empty-chart">
              <span>NO COMPLEXITY DATA</span>
            </div>
          ) : (
            <div className="complexity-usage-list">

              {complexity.map((item) => {

                const percentage =
                  totalComplexityRequests > 0
                    ? (
                        (Number(item.requests) /
                          totalComplexityRequests) *
                        100
                      )
                    : 0;

                return (
                  <div
                    className="complexity-usage-row"
                    key={item.complexity}
                  >

                    <span
                      className={`complexity-label complexity-${item.complexity}`}
                    >
                      {item.complexity}
                    </span>

                    <div className="complexity-bar">
                      <span
                        style={{
                          width: `${percentage}%`,
                        }}
                      />
                    </div>

                    <span>
                      {formatNumber(item.requests)}
                    </span>

                    <span>
                      {percentage.toFixed(1)}%
                    </span>

                  </div>
                );
              })}

            </div>
          )}

        </section>

      </div>


      {/* TOKEN USAGE */}

      <section className="analytics-panel analytics-token-panel">

        <div className="dashboard-section-header">
          <div>
            <span className="dashboard-section-kicker">
              TOKEN USAGE
            </span>

            <h2>Consumption overview</h2>
          </div>
        </div>


        <div className="token-overview">

          <div className="token-stat">
            <span>INPUT TOKENS</span>

            <strong>
              {formatNumber(
                summary?.total_input_tokens
              )}
            </strong>
          </div>


          <div className="token-divider" />


          <div className="token-stat">
            <span>OUTPUT TOKENS</span>

            <strong>
              {formatNumber(
                summary?.total_output_tokens
              )}
            </strong>
          </div>


          <div className="token-divider" />


          <div className="token-stat">
            <span>TOTAL TOKENS</span>

            <strong>
              {formatNumber(
                summary?.total_tokens
              )}
            </strong>
          </div>

        </div>

      </section>

    </div>
  );
}


export default AnalyticsPage;