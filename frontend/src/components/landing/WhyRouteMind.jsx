function WhyRouteMind() {
  return (
    <section className="section why-section" id="routing">
      <div className="section-heading">
        <span className="section-index">01</span>

        <div>
          <p className="section-kicker">WHY ROUTEMIND</p>

          <h2>
            One question.
            <br />
            <span>One intelligent route.</span>
          </h2>
        </div>

        <p className="section-description">
          Different questions need different levels of intelligence.
          RouteMind decides how much model power your request actually needs.
        </p>
      </div>

      <div className="principles-grid">
        <article className="principle">
          <span className="principle-number">01</span>

          <div>
            <h3>Understand</h3>
            <p>
              Every request is analyzed for complexity before a model is
              selected.
            </p>
          </div>
        </article>

        <article className="principle">
          <span className="principle-number">02</span>

          <div>
            <h3>Route</h3>
            <p>
              RouteMind chooses a model tier that matches the actual task.
            </p>
          </div>
        </article>

        <article className="principle">
          <span className="principle-number">03</span>

          <div>
            <h3>Verify</h3>
            <p>
              Responses can be evaluated so quality remains part of the
              routing decision.
            </p>
          </div>
        </article>

        <article className="principle">
          <span className="principle-number">04</span>

          <div>
            <h3>Measure</h3>
            <p>
              Cost, latency, tokens, and model usage are tracked for every
              request.
            </p>
          </div>
        </article>
      </div>
    </section>
  );
}

export default WhyRouteMind;