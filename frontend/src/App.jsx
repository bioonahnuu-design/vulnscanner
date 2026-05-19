import "./App.css";
import { useState } from "react";
import axios from "axios";
import jsPDF from "jspdf";
import "canvg";
import React from "react";

export default function App() {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  // SCAN FUNCTION
  const handleScan = async () => {
    if (!target) return;

    setLoading(true);
    setAiLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/scan",
        {
          target: target,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      console.log("SUCCESS:", response.data);

      setResult(response.data);

      setHistory((prev) => [response.data, ...prev]);
    } catch (error) {
      console.log("FULL ERROR:", error);

      alert(error.response?.data?.error || error.message || "Scan failed");
    } finally {
      setLoading(false);
      setAiLoading(false);
    }
  };

  // PDF REPORT
  const downloadPDF = () => {
    if (!result) return;

    const doc = new jsPDF();

    doc.setFontSize(20);

    doc.text("AI Security Report", 20, 20);

    doc.setFontSize(12);

    doc.text(`Target: ${result.target}`, 20, 40);

    doc.text(`IP Address: ${result.ip}`, 20, 50);

    doc.text(`Risk Level: ${result.risk}`, 20, 60);

    // PORTS
    let portsText = result.ports
      .map((p) => `${p.port} (${p.service})`)
      .join(", ");

    doc.text(`Open Ports: ${portsText}`, 20, 80);

    // VULNS
    let vulnText =
      result.vulnerabilities.length > 0
        ? result.vulnerabilities.map((v) => `${v.port}: ${v.issue}`).join(", ")
        : "No critical vulnerabilities";

    doc.text(`Vulnerabilities: ${vulnText}`, 20, 100);

    // AI ANALYSIS
    const aiLines = doc.splitTextToSize(
      result.ai_analysis || "No AI analysis",
      170,
    );

    doc.text(aiLines, 20, 130);

    doc.save("security-report.pdf");
  };

  return (
    <div className="app">
      <div className="bg-glow"></div>

      {/* NAVBAR */}
      <div className="navbar">
        <h1>⚡ VulnScanner</h1>

        <a
          href="https://github.com/nahnurohmania/vulnscanner"
          target="_blank"
          rel="noreferrer"
          className="github-btn"
        >
          Github
        </a>
      </div>

      {/* HERO */}
      <div className="hero">
        <div className="hero-left">
          <p className="tag">CYBER SECURITY DASHBOARD</p>

          <h2>
            Modern Vulnerability
            <span> Scanner UI</span>
          </h2>

          <p className="desc">
            Scan open ports, analyze HTTP headers, and visualize security
            exposure with a futuristic cyberpunk dashboard.
          </p>

          {/* SCAN BOX */}
          <div className="scan-box">
            <input
              type="text"
              placeholder="Enter target..."
              value={target}
              onChange={(e) => setTarget(e.target.value)}
            />

            <button onClick={handleScan}>
              {loading ? (
                <div className="scan-loading">
                  <div className="spinner"></div>

                  <span>Scanning...</span>
                </div>
              ) : (
                "Start Scan"
              )}
            </button>
          </div>
        </div>

        {/* RIGHT CARD */}
        <div className="hero-right">
          <div className={`glass-card ${result?.risk?.toLowerCase()}`}>
            <p>{result ? "Target" : "System Status"}</p>

            {result && <div className="status-badge">🟢 SCAN COMPLETED</div>}

            <h3>{result?.target || "🎯 Ready to scan target"}</h3>

            <div className="mini-grid">
              <div>
                <span>IP</span>

                <h4>{result?.ip || "---"}</h4>
              </div>

              <div>
                <span>Risk</span>

                <h4 className={`risk ${result?.risk?.toLowerCase()}`}>
                  {result?.risk || "---"}
                </h4>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* RESULTS */}
      {result && (
        <>
          {/* OPEN PORTS */}
          <div className="ports-section">
            <h2>🛡️ Open Ports</h2>

            <div className="ports-grid">
              {result?.ports?.map((item, index) => (
                <div className="port-card" key={index}>
                  <h3>{item.port}</h3>

                  <p>{item.service}</p>
                </div>
              ))}
            </div>
          </div>

          {/* HEADERS */}
          <div className="headers-section">
            <h2>🌐 HTTP Headers</h2>

            <div className="headers-grid">
              {result?.headers &&
                Object.entries(result.headers).map(([key, value]) => (
                  <div className="header-card" key={key}>
                    <h4>{key}</h4>

                    <p>{value}</p>
                  </div>
                ))}
            </div>
          </div>

          {/* VULNS */}
          <div className="headers-section">
            <h2>⚠️ Detected Vulnerabilities</h2>

            <div className="headers-grid">
              {result?.vulnerabilities?.length > 0 ? (
                result.vulnerabilities.map((item, index) => (
                  <div className="header-card" key={index}>
                    <h4>Port {item.port}</h4>

                    <p>{item.issue}</p>
                  </div>
                ))
              ) : (
                <div className="header-card">
                  <h4>No Critical Vulnerabilities</h4>

                  <p>Target appears relatively safe.</p>
                </div>
              )}
            </div>
          </div>

          {/* AI */}
          <div className="headers-section">
            <h2>🤖 AI Security Analysis</h2>

            <div className="headers-grid">
              <div className="header-card ai-card">
                {aiLoading ? (
                  <div className="ai-loading">
                    <div className="spinner"></div>

                    <p>🤖 AI is analyzing vulnerabilities...</p>
                  </div>
                ) : (
                  <div className="ai-text">
                    {result?.ai_analysis?.split("\n").map((line, index) => (
                      <p key={index}>{line}</p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* PDF */}
          <div className="report-section">
            <button className="report-btn" onClick={downloadPDF}>
              📄 Download Security Report
            </button>
          </div>

          {/* HISTORY */}
          <div className="headers-section">
            <h2>🕘 Recent Scans</h2>

            <div className="headers-grid">
              {history.map((item, index) => (
                <div className="header-card" key={index}>
                  <h4>{item.target}</h4>

                  <p>IP: {item.ip}</p>

                  <p>Risk: {item.risk}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* FOOTER */}
      <footer className="footer">
        <p>Built with React + Flask</p>

        <span>by Nahnu Rohmania</span>
      </footer>
    </div>
  );
}
