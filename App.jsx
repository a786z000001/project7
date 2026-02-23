import { useState } from "react";
import axios from "axios";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const getRiskLabel = (score) => {
    if (score < 0.3) return "Low Risk";
    if (score < 0.6) return "Moderate Risk";
    return "High Risk";
  };

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8001/score", {
        response_text: text,
      });
      setResult(res.data);
    } catch (err) {
      alert("Backend not reachable. Make sure FastAPI is running.");
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "white",
        padding: "40px",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ fontSize: "28px", marginBottom: "20px" }}>
        LLM Hallucination Risk Analyzer
      </h1>

      <textarea
        rows="6"
        style={{
          width: "100%",
          padding: "15px",
          borderRadius: "8px",
          background: "#1e293b",
          color: "white",
          border: "1px solid #334155",
        }}
        placeholder="Paste LLM output or ask a question..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={analyze}
        style={{
          marginTop: "15px",
          padding: "10px 20px",
          background: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div
          style={{
            marginTop: "30px",
            display: "flex",
            flexDirection: "column",
            gap: "20px",
          }}
        >
          {/* Answer Box */}
          {result.answer && (
            <div
              style={{
                background: "#1e293b",
                padding: "20px",
                borderRadius: "8px",
                borderLeft:
                  result.claim_type === "factual"
                    ? "4px solid #10b981"
                    : "4px solid #f59e0b",
              }}
            >
              <h3
                style={{
                  marginTop: 0,
                  marginBottom: "10px",
                  color: "#94a3b8",
                }}
              >
                {result.claim_type === "factual"
                  ? "Exact Factual Answer:"
                  : "Educated Guess:"}
              </h3>
              <p
                style={{
                  margin: 0,
                  fontSize: "1.1em",
                  lineHeight: "1.5",
                }}
              >
                {result.answer}
              </p>
            </div>
          )}

          {/* Scorer Box */}
          <div
            style={{
              background: "#1e293b",
              padding: "20px",
              borderRadius: "8px",
              display: "flex",
              gap: "40px",
              alignItems: "center",
            }}
          >
            <div style={{ width: 140 }}>
              <CircularProgressbar
                value={(result.hallucination_score ?? 0) * 100}
                text={`${((result.hallucination_score ?? 0) * 100).toFixed(
                  3
                )}%`}
                styles={buildStyles({
                  pathColor:
                    result.hallucination_score < 0.3
                      ? "#10b981"
                      : result.hallucination_score < 0.6
                      ? "#f59e0b"
                      : "#ef4444",
                  textColor: "#fff",
                  trailColor: "#334155",
                })}
              />
              <p
                style={{
                  marginTop: "10px",
                  textAlign: "center",
                  fontWeight: "bold",
                  color: "#fff",
                }}
              >
                {getRiskLabel(result.hallucination_score ?? 0)}
              </p>
            </div>

            <div>
              <p>
                <b>Contradiction Ratio:</b>{" "}
                {Number(result.contradiction_ratio ?? 0).toFixed(3)}
              </p>
              <p>
                <b>Unknown Ratio:</b>{" "}
                {Number(result.unknown_ratio ?? 0).toFixed(3)}
              </p>
              <p>
                <b>Entropy Score:</b>{" "}
                {Number(result.entropy_score ?? 0).toFixed(3)}
              </p>
              <p>
                <b>Variance Score:</b>{" "}
                {Number(result.variance_score ?? 0).toFixed(3)}
              </p>
              <p>
                <b>Confidence:</b>{" "}
                {Number(result.confidence ?? 0).toFixed(3)}
              </p>
              <p>
                <b>Verdict:</b> {result.verdict ?? "N/A"}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}