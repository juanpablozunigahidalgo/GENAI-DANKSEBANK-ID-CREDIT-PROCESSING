import { useState } from "react";
import { checkRegistry } from "../api/bank";

export default function Registry() {
  const [nationalId, setNationalId] = useState("");
  const [country, setCountry] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleSearch = async () => {
    try {
      const res = await checkRegistry(nationalId, country);
      setResult(res);
    } catch {
      setResult({ error: "Could not fetch registry info." });
    }
  };

  return (
    <main
      style={{
        backgroundColor: "#fff",
        minHeight: "100vh",
        paddingTop: "5rem",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "500px",
          background: "white",
          borderRadius: "12px",
          padding: "2rem",
          boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
        }}
      >
        <h2>Check National Registry</h2>
        <input
          type="text"
          placeholder="National ID"
          value={nationalId}
          onChange={(e) => setNationalId(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem",
            marginTop: "1rem",
            marginBottom: "0.5rem",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        />
        <input
          type="text"
          placeholder="Country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{
            width: "100%",
            padding: "0.5rem",
            marginBottom: "1rem",
            border: "1px solid #ccc",
            borderRadius: "6px",
          }}
        />
        <button
          onClick={handleSearch}
          style={{
            background: "#0b5fa5",
            color: "#fff",
            border: "none",
            padding: "0.6rem 1.2rem",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          Search
        </button>

        {result && (
          <div style={{ marginTop: "1.5rem" }}>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}
