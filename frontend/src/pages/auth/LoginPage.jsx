import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import AuthForm from "../../components/auth/AuthForm";
import { loginUser} from "../../services/authService";
import { useAuth } from "../../context/AuthContext";

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await loginUser({
        email: formData.email,
        password: formData.password,
      });

      await login(data.access_token);

      navigate("/dashboard");
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-page">
      <div className="auth-shell">
        <div className="auth-brand">
          <Link to="/" className="brand">
            <span className="brand-mark" />
            <span className="brand-name">ROUTEMIND</span>
          </Link>
        </div>

        <section className="auth-panel">
          <div className="auth-header">
            <span className="auth-index">AUTH / 01</span>

            <h1>Welcome back.</h1>

            <p>
              Sign in to route your requests intelligently.
            </p>
          </div>

          <AuthForm
            mode="login"
            email={formData.email}
            password={formData.password}
            onChange={handleChange}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />

          <div className="auth-switch">
            <span>Don't have an account?</span>

            <Link to="/register">
              Create one →
            </Link>
          </div>
        </section>

        <div className="auth-status">
          <span className="status-dot" />
          ROUTEMIND SYSTEM READY
        </div>
      </div>
    </main>
  );
}

export default LoginPage;