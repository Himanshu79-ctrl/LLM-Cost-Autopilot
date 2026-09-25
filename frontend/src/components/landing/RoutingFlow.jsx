const steps = [
  {
    number: "01",
    label: "ANALYZE",
    title: "Complexity",
  },
  {
    number: "02",
    label: "ROUTE",
    title: "Best model",
  },
  {
    number: "03",
    label: "GENERATE",
    title: "Response",
  },
  {
    number: "04",
    label: "VERIFY",
    title: "Quality",
  },
];

function RoutingFlow() {
  return (
    <div className="routing-flow">
      {steps.map((step, index) => (
        <div className="routing-step-wrapper" key={step.number}>
          <div className="routing-step">
            <span className="routing-number">{step.number}</span>

            <div>
              <span className="routing-label">{step.label}</span>
              <strong>{step.title}</strong>
            </div>
          </div>

          {index < steps.length - 1 && (
            <span className="routing-arrow">→</span>
          )}
        </div>
      ))}
    </div>
  );
}

export default RoutingFlow;