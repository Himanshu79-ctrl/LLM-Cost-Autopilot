const models = [
  {
    level: "LOW",
    title: "Fast & efficient",
    description:
      "Straightforward questions can use a lightweight model without wasting expensive compute.",
    signal: "CHEAP",
  },
  {
    level: "MEDIUM",
    title: "Balanced reasoning",
    description:
      "More involved requests are routed to a model with additional reasoning capability.",
    signal: "BALANCED",
  },
  {
    level: "HIGH",
    title: "Maximum capability",
    description:
      "Complex technical and multi-step requests can be routed to a more capable model.",
    signal: "POWERFUL",
  },
];

function ModelRouting() {
  return (
    <section className="section model-section">
      <div className="section-heading">
        <span className="section-index">03</span>

        <div>
          <p className="section-kicker">MODEL ROUTING</p>

          <h2>
            Not every question
            <br />
            <span>needs the same model.</span>
          </h2>
        </div>

        <p className="section-description">
          RouteMind adjusts model selection according to the complexity of the
          request instead of sending everything to the most expensive model.
        </p>
      </div>

      <div className="model-grid">
        {models.map((model, index) => (
          <article
            className={`model-card ${
              index === 1 ? "model-card-active" : ""
            }`}
            key={model.level}
          >
            <div className="model-card-top">
              <span>{model.level}</span>

              <span className="model-signal">
                {model.signal}
              </span>
            </div>

            <h3>{model.title}</h3>

            <p>{model.description}</p>

            <div className="model-meter">
              <span
                style={{
                  width:
                    index === 0
                      ? "32%"
                      : index === 1
                        ? "61%"
                        : "92%",
                }}
              />
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default ModelRouting;