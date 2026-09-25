import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import AuthForm from "../../components/auth/AuthForm";
import {
  registerUser,
} from "../../services/authService";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
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

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      const data = await registerUser({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      });
      navigate("/login");
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
            <span className="auth-index">AUTH / 02</span>

            <h1>Create your account.</h1>

            <p>
              Start routing requests with intelligence, cost awareness,
              and measurable performance.
            </p>
          </div>

          <AuthForm
            mode="register"
            name={formData.name}
            email={formData.email}
            password={formData.password}
            confirmPassword={formData.confirmPassword}
            onChange={handleChange}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />

          <div className="auth-switch">
            <span>Already have an account?</span>

            <Link to="/login">
              Log in →
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

export default RegisterPage;