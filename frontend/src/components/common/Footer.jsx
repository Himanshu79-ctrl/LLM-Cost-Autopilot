function Footer() {
  return (
    <footer className="footer">
      <div className="footer-main">
        <div className="footer-brand">
          <a href="/" className="brand">
            <span className="brand-mark" />
            <span className="brand-name">ROUTEMIND</span>
          </a>

          <p>
            Intelligent LLM routing for better answers,
            lower costs, and measurable performance.
          </p>
        </div>

        <div className="footer-column">
          <span>PRODUCT</span>

          <a href="#product">Ask RouteMind</a>
          <a href="#routing">Routing</a>
          <a href="#how-it-works">How it works</a>
        </div>

        <div className="footer-column">
          <span>PLATFORM</span>

          <a href="/">Analytics</a>
          <a href="/">Models</a>
          <a href="/">Requests</a>
        </div>

        <div className="footer-column">
          <span>ACCOUNT</span>

          <a href="/">Log in</a>
          <a href="/">Get started</a>
        </div>
      </div>

      <div className="footer-bottom">
        <span>© 2026 RouteMind</span>

        <span className="footer-status">
          <i />
          SYSTEM READY
        </span>

        <span>LLM COST AUTOPILOT</span>
      </div>
    </footer>
  );
}

export default Footer;