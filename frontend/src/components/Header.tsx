import { Link, useLocation } from "react-router-dom";
import "../styles/layout.css";

export default function Header() {
  const { pathname } = useLocation();

  const linkClass = (path: string) =>
    pathname === path ? "nav-link active" : "nav-link";

  return (
    <header className="topbar">
      <div className="logo">Danske Bank</div>
      <nav>
        <Link to="/" className={linkClass("/")}>
          Home
        </Link>
        <Link to="/customers" className={linkClass("/customers")}>
          Customers
        </Link>
        <Link to="/registry" className={linkClass("/registry")}>
          Registry
        </Link>
      </nav>
      <button className="login-btn">Logga in 🔒</button>
    </header>
  );
}
