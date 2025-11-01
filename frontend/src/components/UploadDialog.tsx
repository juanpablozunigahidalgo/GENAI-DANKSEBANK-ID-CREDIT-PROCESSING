import { useState } from "react";
import { uploadId } from "../api/bank";

interface Props {
  open: boolean;
  onClose: () => void;
  onUploaded: (res: any) => void;
}

export default function UploadDialog({ open, onClose, onUploaded }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      // 👇 remember: backend needs user_id in query
      const res = await uploadId(file, "string");
      onUploaded(res);
      onClose();
    } catch (err) {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      // backdrop
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.35)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 2000,
      }}
    >
      <div
        // modal
        style={{
          background: "#fff",
          borderRadius: "0.9rem",
          width: "340px",
          maxWidth: "90vw",
          boxShadow: "0 20px 40px rgba(0,0,0,0.25)",
          padding: "1.2rem 1.2rem 1rem",
          fontFamily:
            'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        }}
      >
        <h3 style={{ marginTop: 0, marginBottom: "0.8rem" }}>
          Upload ID Document
        </h3>
        <p style={{ fontSize: "0.78rem", marginBottom: "0.7rem" }}>
          Please attach the ID document the agent asked for.
        </p>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          style={{ marginBottom: "1rem" }}
        />

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            gap: "0.6rem",
          }}
        >
          <button
            onClick={onClose}
            style={{
              background: "transparent",
              border: "1px solid #ccc",
              borderRadius: "6px",
              padding: "0.35rem 0.8rem",
              cursor: "pointer",
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            style={{
              background: !file || loading ? "#b7d3eb" : "#0b5fa5",
              border: "none",
              color: "white",
              borderRadius: "6px",
              padding: "0.35rem 0.8rem",
              cursor: !file || loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
}
