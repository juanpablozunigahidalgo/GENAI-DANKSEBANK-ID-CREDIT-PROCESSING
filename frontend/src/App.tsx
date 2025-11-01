import { Outlet, Link, useLocation } from "react-router-dom";
import ChatWidget from "./components/ChatWidget";

export default function App() {
  const location = useLocation();
  const showChat = location.pathname === "/";

  return (
    <>
      <nav
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          background: "#e6e6da",
          padding: "0.4rem 1rem",
          zIndex: 100,
        }}
      >
        <Link to="/" style={{ marginRight: "1rem" }}>
          Home
        </Link>
        <Link to="/customers" style={{ marginRight: "1rem" }}>
          Customers
        </Link>
        <Link to="/registry">Registry</Link>
      </nav>

      <div style={{ marginTop: "40px" }}>
        <Outlet />
      </div>

      {showChat && <ChatWidget />}
    </>
  );
}
