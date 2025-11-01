import { useEffect, useRef, useState } from "react";
import { chatWithAgent } from "../api/bank";
import UploadDialog from "./UploadDialog";

type ChatMessage = {
  from: "user" | "agent";
  text: string;
};

export default function ChatWidget() {
  const [open, setOpen] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [showUpload, setShowUpload] = useState(false);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // 🔎 make detection very forgiving
  const shouldAskForUpload = (text: string) => {
    if (!text) return false;
    // Normalize: remove newlines, multiple spaces, and lowercase
    const normalized = text.replace(/\s+/g, " ").toLowerCase();

    // check for any upload-related keyword
    return (
      normalized.includes("upload") ||
      normalized.includes("id document") ||
      normalized.includes("id documents") ||
      normalized.includes("provide your documents") ||
      normalized.includes("please attach") ||
      normalized.includes("required documents")
    );
  };

  // init: first message from backend
  useEffect(() => {
    const init = async () => {
      try {
        const res = await chatWithAgent("hello", "string");
        const msg = res.answer ?? "Hello! Welcome to Danske Bank.";
        setMessages([{ from: "agent", text: msg }]);

        // 👇 if first message already asks to upload → open
        if (shouldAskForUpload(msg)) {
          setShowUpload(true);
        }
      } catch (e) {
        setMessages([
          {
            from: "agent",
            text: "Sorry, I could not connect to the backend.",
          },
        ]);
      }
    };
    init();
  }, []);

  // auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userText = input.trim();
    setInput("");

    setMessages((prev) => [...prev, { from: "user", text: userText }]);

    try {
      const res = await chatWithAgent(userText, "string");
      const agentMsg = res.answer ?? "";
      setMessages((prev) => [...prev, { from: "agent", text: agentMsg }]);

      // 👇 if agent replies "please upload..." → open dialog
      if (shouldAskForUpload(agentMsg)) {
        setShowUpload(true);
      }
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { from: "agent", text: "Error talking to backend." },
      ]);
    }
  };

  const handleUploaded = async (_res: any) => {
    // tell the agent we uploaded
    const res = await chatWithAgent("I have uploaded my ID.", "string");
    const agentMsg = res.answer ?? "";
    setMessages((prev) => [...prev, { from: "agent", text: agentMsg }]);

    // maybe agent asks again (bad doc) → re-open
    if (shouldAskForUpload(agentMsg)) {
      setShowUpload(true);
    }
  };

  return (
    <>
      <div
        style={{
          position: "fixed",
          right: "1.5rem",
          bottom: "1.5rem",
          width: open ? "360px" : "240px",
          background: "#ffffff",
          borderRadius: "1rem",
          boxShadow: "0 20px 40px rgba(0,0,0,0.18)",
          overflow: "hidden",
          fontFamily:
            'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          zIndex: 999,
        }}
      >
        {/* header */}
        <div
          onClick={() => setOpen((o) => !o)}
          style={{
            background: "#0b5fa5",
            color: "#fff",
            padding: "0.65rem 0.85rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            cursor: "pointer",
          }}
        >
          <div>
            <div style={{ fontSize: "0.9rem", fontWeight: 600 }}>
              Onboarding Assistant
            </div>
            <div style={{ fontSize: "0.65rem", opacity: 0.85 }}>
              Danske Bank · Credit mock
            </div>
          </div>
          <button
            style={{
              background: "rgba(255,255,255,0.12)",
              border: "none",
              color: "#fff",
              borderRadius: "999px",
              width: "26px",
              height: "26px",
              cursor: "pointer",
            }}
          >
            {open ? "▾" : "▴"}
          </button>
        </div>

        {/* body */}
        {open && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              height: "420px",
              background: "#f6f7f9",
            }}
          >
            <div
              style={{
                flex: 1,
                padding: "0.6rem",
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                gap: "0.4rem",
              }}
            >
              {messages.map((m, i) => (
                <div
                  key={i}
                  style={{
                    maxWidth: "90%",
                    alignSelf: m.from === "user" ? "flex-end" : "flex-start",
                    background: m.from === "user" ? "#0b5fa5" : "white",
                    color: m.from === "user" ? "white" : "black",
                    padding: "0.4rem 0.6rem",
                    borderRadius:
                      m.from === "user"
                        ? "0.6rem 0.1rem 0.6rem 0.6rem"
                        : "0.1rem 0.6rem 0.6rem 0.6rem",
                    fontSize: "0.82rem",
                    border:
                      m.from === "agent"
                        ? "1px solid rgba(0,0,0,0.03)"
                        : "none",
                  }}
                >
                  {m.text}
                </div>
              ))}
              <div ref={bottomRef} />
            </div>

            {/* input */}
            <div
              style={{
                display: "flex",
                gap: "0.4rem",
                padding: "0.5rem",
                background: "white",
                borderTop: "1px solid #e5e5e5",
              }}
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                placeholder="Type your message..."
                style={{
                  flex: 1,
                  border: "1px solid #d3d3d3",
                  borderRadius: "0.4rem",
                  padding: "0.3rem 0.5rem",
                  fontSize: "0.78rem",
                }}
              />
              <button
                onClick={sendMessage}
                style={{
                  background: "#0b5fa5",
                  border: "none",
                  color: "white",
                  borderRadius: "0.4rem",
                  padding: "0 0.8rem",
                  cursor: "pointer",
                  fontSize: "0.78rem",
                }}
              >
                Send
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 👇 modal de subida */}
      <UploadDialog
        open={showUpload}
        onClose={() => setShowUpload(false)}
        onUploaded={handleUploaded}
      />
    </>
  );
}
