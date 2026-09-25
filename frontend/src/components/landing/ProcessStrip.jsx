const processSteps = [
  ["01", "Analyze every request"],
  ["02", "Route by complexity"],
  ["03", "Verify the result"],
  ["04", "Track the cost"],
];

function ProcessStrip() {
  return (
    <section className="process-strip" id="how-it-works">
      {processSteps.map(([number, label]) => (
        <div className="process-item" key={number}>
          <span className="process-number">
            {number}
          </span>

          <span className="process-label">
            {label}
          </span>
        </div>
      ))}
    </section>
  );
}

export default ProcessStrip;