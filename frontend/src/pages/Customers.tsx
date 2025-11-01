import { useEffect, useState } from "react";
import { getAllCustomers } from "../api/bank";
import "../styles/layout.css";

export default function Customers() {
  const [customers, setCustomers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllCustomers()
      .then((data) => setCustomers(data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main
      style={{
        backgroundColor: "#ffffff",
        minHeight: "100vh",
        paddingTop: "5rem",
        paddingLeft: "2rem",
        paddingRight: "2rem",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "0 auto",
          background: "white",
          borderRadius: "12px",
          padding: "2rem",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
        }}
      >
        <h2 style={{ marginBottom: "1.5rem" }}>Registered Customers</h2>

        {loading ? (
          <p>Loading...</p>
        ) : customers.length === 0 ? (
          <p>No customers found.</p>
        ) : (
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              fontSize: "0.95rem",
            }}
          >
            <thead>
              <tr
                style={{
                  backgroundColor: "#f4f4f4",
                  textAlign: "left",
                  borderBottom: "2px solid #ddd",
                }}
              >
                <th style={{ padding: "0.75rem" }}>Name</th>
                <th style={{ padding: "0.75rem" }}>Email</th>
                <th style={{ padding: "0.75rem" }}>Country</th>
                <th style={{ padding: "0.75rem" }}>National ID</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((c, i) => (
                <tr
                  key={i}
                  style={{
                    borderBottom: "1px solid #eee",
                    background: i % 2 === 0 ? "#fff" : "#fafafa",
                  }}
                >
                  <td style={{ padding: "0.75rem" }}>
                    {(c.firstName || c.first_name) +
                      " " +
                      (c.lastName || c.last_name)}
                  </td>
                  <td style={{ padding: "0.75rem" }}>{c.email}</td>
                  <td style={{ padding: "0.75rem" }}>{c.country}</td>
                  <td style={{ padding: "0.75rem" }}>{c.national_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </main>
  );
}
