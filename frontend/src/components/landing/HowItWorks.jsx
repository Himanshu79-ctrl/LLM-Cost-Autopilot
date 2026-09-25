const steps = [
  {
    number: "01",
    title: "Your question arrives",
    description:
      "You send RouteMind a normal prompt. No need to decide which model to use.",
  },
  {
    number: "02",
    title: "Complexity is analyzed",
    description:
      "RouteMind evaluates the request and determines how demanding the task is.",
  },
  {
    number: "03",
    title: "A model is selected",
    description:
      "The routing engine maps the request to an appropriate model tier.",
  },
  {
    number: "04",
    title: "The answer is verified",
    description:
      "The response can be evaluated and escalated when the result needs another level of reasoning.",
  },
];

function HowItWorks() {
  return (
    <section className="section how-section" id="how-it-works">
      <div className="section-heading compact-heading">
        <span className="section-index">02</span>

        <div>
          <p className="section-kicker">HOW IT WORKS</p>

          <h2>
            The route happens
            <br />
            <span>behind the scenes.</span>
          </h2>
        </div>
      </div>

      <div className="how-grid">
        {steps.map((step) => (
          <article className="how-step" key={step.number}>
            <span className="how-number">{step.number}</span>

            <div className="how-line" />

            <h3>{step.title}</h3>

            <p>{step.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default HowItWorks;