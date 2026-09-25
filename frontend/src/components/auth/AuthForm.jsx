function AuthForm({
  mode,
  name,
  email,
  password,
  confirmPassword,
  onChange,
  onSubmit,
  loading,
  error,
}) {
  const isRegister = mode === "register";

  return (
    <form className="auth-form" onSubmit={onSubmit}>
      {isRegister && (
        <div className="form-field">
          <label htmlFor="name">Name</label>

          <input
            id="name"
            name="name"
            type="text"
            placeholder="Your name"
            value={name}
            onChange={onChange}
            autoComplete="name"
            required
          />
        </div>
      )}

      <div className="form-field">
        <label htmlFor="email">Email</label>

        <input
          id="email"
          name="email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={onChange}
          autoComplete="email"
          required
        />
      </div>

      <div className="form-field">
        <label htmlFor="password">Password</label>

        <input
          id="password"
          name="password"
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={onChange}
          autoComplete={isRegister ? "new-password" : "current-password"}
          required
        />
      </div>

      {isRegister && (
        <div className="form-field">
          <label htmlFor="confirmPassword">Confirm password</label>

          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            placeholder="Confirm your password"
            value={confirmPassword}
            onChange={onChange}
            autoComplete="new-password"
            required
          />
        </div>
      )}

      {error && (
        <div className="auth-error" role="alert">
          {error}
        </div>
      )}

      <button
        type="submit"
        className="auth-submit"
        disabled={loading}
      >
        {loading
          ? "Please wait..."
          : isRegister
            ? "Create account →"
            : "Log in →"}
      </button>
    </form>
  );
}

export default AuthForm;