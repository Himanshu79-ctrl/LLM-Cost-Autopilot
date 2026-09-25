function Button({
  children,
  variant = "primary",
  className = "",
  onClick,
}) {
  return (
    <button
      type="button"
      className={`button button-${variant} ${className}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default Button;