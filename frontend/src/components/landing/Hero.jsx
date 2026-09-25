import Button from "../common/Button";

function Hero() {
  return (
    <section className="hero">
      <div className="hero-eyebrow">
        <span className="eyebrow-line" />
        LLM COST AUTOPILOT
      </div>

      <h1>
        Ask anything.
        <br />
        <span>Route intelligently.</span>
      </h1>

      <p className="hero-description">
        RouteMind analyzes every prompt, selects the right model for the task,
        and verifies the response — balancing quality, speed, and cost
        automatically.
      </p>

      <div className="hero-actions">
        <Button className="hero-primary">
          Route your first prompt <span>→</span>
        </Button>

        <Button variant="secondary">
          See how routing works
        </Button>
      </div>
    </section>
  );
}

export default Hero;