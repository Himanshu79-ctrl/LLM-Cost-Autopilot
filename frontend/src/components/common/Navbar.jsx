import { Link } from "react-router-dom";
import Logo from "./Logo";
import Button from "./Button";

function Navbar() {
  return (
    <header className="navbar">
      <Logo />

      <nav className="nav-links" aria-label="Main navigation">
        <a href="#product">Product</a>
        <a href="#routing">Routing</a>
        <a href="#how-it-works">How it works</a>
      </nav>

      <div className="nav-actions">
        <Link to="/login" className="login-button">
          Log in
        </Link>

        <Link to="/register" className="nav-start-link">
          <Button>
            Get started <span>→</span>
          </Button>
        </Link>
      </div>
    </header>
  );
}

export default Navbar;