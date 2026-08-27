import { useState } from "react";
import { authRequests } from "../api/client";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await authRequests("/auth/signup", {
        method: "POST",
        body: {
          name,
          email,
          password,
        },
      });
      navigate("/login");
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main">
      <h1>Banter</h1>
      <div className="auth-page">
        <form className="auth-form" onSubmit={handleSubmit}>
          <h2>Register</h2>
          <input
            className="auth-input"
            type="text"
            placeholder="Enter your name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            className="auth-input"
            type="email"
            placeholder="Enter your email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            className="auth-input"
            type="password"
            placeholder="Enter your password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          ></input>
          {error && <p className="error">{error}</p>}
          <button type="submit" disabled={loading}>
            {loading ? "Loading..." : "Register"}
          </button>

          <Link to="/login">Already have an account?</Link>
        </form>
      </div>
    </div>
  );
}

export default Register;
