import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
const APP_VERSION = "2.0.0";

function getRiskClass(risk = "") {
  return risk.toLowerCase();
}

function formatTimestamp(value) {
  if (!value) return "Not scanned";

  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "medium",
  }).format(new Date(value));
}

export default function App() {
  const [target, setTarget] = useState("");
  const [authorized, setAuthorized] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [backendStatus, setBackendStatus] = useState(
    API_URL ? "checking" : "offline",
  );

  useEffect(() => {
    if (!API_URL) {
      return undefined;
    }

    const controller = new AbortController();

    async function checkBackend() {
      try {
        const response = await fetch(`${API_URL}/health`, {
          signal: controller.signal,
        });
        setBackendStatus(response.ok ? "online" : "offline");
      } catch {
        if (!controller.signal.aborted) setBackendStatus("offline");
      }
    }

    checkBackend();
    return () => controller.abort();
  }, []);

  const summary = useMemo(
    () => ({
      ports: result?.ports?.length ?? "-",
      findings: result?.vulnerabilities?.length ?? "-",
      headers: Object.keys(result?.headers || {}).length,
    }),
    [result],
  );

  async function handleScan(event) {
    event.preventDefault();
    const cleanTarget = target.trim();

    if (!cleanTarget) {
      setError("Enter a hostname or IP address first.");
      return;
    }

    if (!authorized) {
      setError("Confirm that you are authorized to scan this target.");
      return;
    }

    if (!API_URL) {
      setError("Backend URL is not configured in frontend/.env.");
      return;
    }

    setLoading(true);
    setError("");

    const startedAt = performance.now();
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 35000);

    try {
      const response = await fetch(`${API_URL}/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: cleanTarget }),
        signal: controller.signal,
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Scan failed.");

      const scanResult = {
        ...data,
        scan_duration: Number(
          ((performance.now() - startedAt) / 1000).toFixed(2),
        ),
        scanned_at: new Date().toISOString(),
      };

      setResult(scanResult);
      setBackendStatus("online");
      setHistory((current) =>
        [
          scanResult,
          ...current.filter((item) => item.target !== scanResult.target),
        ].slice(0, 4),
      );
    } catch (requestError) {
      if (requestError.name === "AbortError") {
        setError("Assessment stopped after the 35-second safety timeout.");
      } else {
        setError(requestError.message || "The backend is unreachable.");
      }
    } finally {
      window.clearTimeout(timeout);
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <div className="grid-background" aria-hidden="true" />
      <div className="background-glow glow-one" aria-hidden="true" />
      <div className="background-glow glow-two" aria-hidden="true" />

      <nav className="navbar">
        <a className="brand" href="#home" aria-label="VulnScanner home">
          <span className="brand-icon">V</span>
          <span className="brand-text">
            Vuln<span>Scanner</span>
          </span>
        </a>

        <div className="nav-actions">
          <span
            className={`api-status ${backendStatus === "online" ? "configured" : "offline"}`}
          >
            <i />
            {backendStatus === "checking"
              ? "CHECKING ENGINE"
              : backendStatus === "online"
                ? "BACKEND ONLINE"
                : "BACKEND OFFLINE"}
          </span>
          <span className="version-badge">v{APP_VERSION}</span>
          <a
            href="https://github.com/bioonahnuu-design/vulnscanner"
            target="_blank"
            rel="noreferrer"
            className="github-button"
          >
            Source code <span>↗</span>
          </a>
        </div>
      </nav>

      <div className="system-strip" aria-label="System information">
        <span>NAHNU SECURITY LAB</span>
        <span>ENGINE / NMAP 7.x</span>
        <span>MODE / DEFENSIVE</span>
        <span>POLICY / AUTHORIZED USE</span>
      </div>

      <section className="hero" id="home">
        <div className="hero-content">
          <div className="eyebrow">
            <span /> NAHNU SECURITY LAB / TOOL 02
          </div>
          <h1>
            Surface the ports.<strong>Explain the risk.</strong>
          </h1>
          <p className="hero-description">
            A focused network exposure assessor built by Nahnu Rohmania. It runs
            targeted Nmap service discovery, reviews HTTP security headers, and
            converts observable signals into defensive remediation notes.
          </p>

          <form className="scan-form" onSubmit={handleScan}>
            <label htmlFor="target">Authorized assessment target</label>
            <div className="scan-control">
              <span className="terminal-prompt">&gt;_</span>
              <input
                id="target"
                type="text"
                placeholder="hostname or IP address"
                value={target}
                onChange={(event) => setTarget(event.target.value)}
                disabled={loading}
                autoComplete="off"
                spellCheck="false"
              />
              <button
                type="submit"
                disabled={loading || backendStatus === "offline"}
              >
                {loading ? (
                  <>
                    <span className="spinner" /> Assessing
                  </>
                ) : (
                  <>
                    Run assessment <span>→</span>
                  </>
                )}
              </button>
            </div>

            <label className="authorization">
              <input
                type="checkbox"
                checked={authorized}
                onChange={(event) => setAuthorized(event.target.checked)}
              />
              <span>
                I own this target or have explicit permission to assess it.
              </span>
            </label>

            {error && (
              <div className="error-message" role="alert">
                <strong>Assessment unavailable</strong>
                <span>{error}</span>
              </div>
            )}
          </form>
        </div>

        <article
          className={`summary-card ${getRiskClass(result?.risk)}`}
          aria-live="polite"
        >
          <header className="terminal-header">
            <div className="terminal-dots" aria-hidden="true">
              <i />
              <i />
              <i />
            </div>
            <span>exposure_summary.json</span>
            <strong>
              {loading ? "RUNNING" : result ? "COMPLETE" : "STANDBY"}
            </strong>
          </header>

          <div className="summary-content">
            <span className="summary-label">
              {result ? "TARGET RESOLVED" : "ASSESSMENT ENGINE"}
            </span>
            <h2>{result?.target || "Ready for authorized input"}</h2>
            <p>
              {result?.ip ||
                "Target validation → Nmap discovery → HTTP probe → risk analysis"}
            </p>
          </div>

          <div className="metrics">
            <div>
              <span>HEURISTIC RISK</span>
              <strong className={`risk ${getRiskClass(result?.risk)}`}>
                {result?.risk || "-"}
              </strong>
            </div>
            <div>
              <span>OPEN PORTS</span>
              <strong>{summary.ports}</strong>
            </div>
            <div>
              <span>FINDINGS</span>
              <strong>{summary.findings}</strong>
            </div>
          </div>

          <div className="scan-metadata">
            <span>
              <small>ENGINE</small>
              {result ? "NMAP VERIFIED" : "NMAP READY"}
            </span>
            <span>
              <small>DURATION</small>
              {result ? `${result.scan_duration}s` : "-"}
            </span>
            <span>
              <small>SCANNED AT</small>
              {result ? formatTimestamp(result.scanned_at) : "-"}
            </span>
          </div>

          <div className="terminal-command">
            <span>$</span> nmap -Pn -sT -sV --version-light{" "}
            {result?.ip || "<target>"}
            <i />
          </div>
        </article>
      </section>

      <section className="capabilities" aria-label="Assessment pipeline">
        <span>
          01 <strong>TARGET VALIDATION</strong>
        </span>
        <span>
          02 <strong>SERVICE DISCOVERY</strong>
        </span>
        <span>
          03 <strong>HEADER ANALYSIS</strong>
        </span>
        <span>
          04 <strong>REMEDIATION</strong>
        </span>
      </section>

      {result && (
        <section className="results" aria-live="polite">
          <div className="section-heading">
            <div>
              <span>
                ASSESSMENT OUTPUT / {formatTimestamp(result.scanned_at)}
              </span>
              <h2>Exposure summary</h2>
            </div>
            <button
              type="button"
              className="report-button"
              onClick={() => window.print()}
            >
              Save report / PDF <span>↓</span>
            </button>
          </div>

          <div className="risk-disclaimer">
            <strong>Interpretation note</strong>
            <p>
              A {result.risk} rating is a heuristic signal based on observable
              services and headers. It is not proof of compromise and should be
              verified manually.
            </p>
          </div>

          <div className="result-grid">
            <ResultPanel title="Discovered services" count={summary.ports}>
              <div className="port-list">
                {result.ports?.length ? (
                  result.ports.map((item) => (
                    <div
                      className="port-row"
                      key={`${item.protocol}-${item.port}`}
                    >
                      <i />
                      <strong>{item.port}</strong>
                      <span>{item.service || "unknown"}</span>
                      <small>
                        {item.protocol?.toUpperCase() || "TCP"} / OPEN
                      </small>
                    </div>
                  ))
                ) : (
                  <EmptyState text="No listed ports responded during this assessment." />
                )}
              </div>
            </ResultPanel>

            <ResultPanel title="Risk signals" count={summary.findings}>
              <div className="finding-list">
                {result.vulnerabilities?.length ? (
                  result.vulnerabilities.map((item) => (
                    <div
                      className="finding-item"
                      key={`${item.port}-${item.issue}`}
                    >
                      <span className="finding-icon">!</span>
                      <div>
                        <strong>
                          {item.severity} / Port {item.port ?? "N/A"}
                        </strong>
                        <p>{item.issue}</p>
                        <small>{item.recommendation}</small>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="finding-item safe">
                    <span className="finding-icon">✓</span>
                    <div>
                      <strong>No configured risk signal detected</strong>
                      <p>
                        Manually verify the target before reaching a security
                        conclusion.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </ResultPanel>

            <ResultPanel
              title="Defensive remediation brief"
              count={
                result.analysis_source === "gemini"
                  ? "GEMINI GENERATED"
                  : "LOCAL FALLBACK"
              }
              wide
            >
              <div className="analysis-text">
                {(result.ai_analysis || "No analysis available.")
                  .split("\n")
                  .filter(Boolean)
                  .map((line, index) => (
                    <p key={index}>{line}</p>
                  ))}
              </div>
            </ResultPanel>

            <ResultPanel
              title="HTTP probe"
              count={result.http?.status_code || "NO RESPONSE"}
              wide
            >
              <div className="http-metadata">
                <span>
                  <small>AVAILABLE</small>
                  {result.http?.available ? "YES" : "NO"}
                </span>
                <span>
                  <small>PROTOCOL</small>
                  {result.http?.protocol?.toUpperCase() || "-"}
                </span>
                <span>
                  <small>STATUS</small>
                  {result.http?.status_code || "-"}
                </span>
                <span>
                  <small>HEADER COUNT</small>
                  {summary.headers}
                </span>
              </div>
              {summary.headers > 0 ? (
                <div className="header-table">
                  {Object.entries(result.headers).map(([key, value]) => (
                    <div className="header-row" key={key}>
                      <strong>{key}</strong>
                      <span>{String(value)}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState text="The target did not return an HTTP response on the tested protocols." />
              )}
            </ResultPanel>
          </div>

          {history.length > 1 && (
            <div className="history">
              <span>SESSION HISTORY / NOT PERSISTED</span>
              <div className="history-list">
                {history.map((item) => (
                  <button
                    type="button"
                    key={`${item.target}-${item.scanned_at}`}
                    onClick={() => setResult(item)}
                  >
                    <span>{item.target}</span>
                    <small>{item.scan_duration}s</small>
                    <small className={`risk ${getRiskClass(item.risk)}`}>
                      {item.risk}
                    </small>
                  </button>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      <footer className="footer">
        <span>VULNSCANNER / v{APP_VERSION}</span>
        <p>
          Designed & engineered by <strong>Nahnu Rohmania</strong>
        </p>
        <span>EDUCATIONAL · DEFENSIVE · AUTHORIZED</span>
      </footer>
    </main>
  );
}

function ResultPanel({ title, count, wide = false, children }) {
  return (
    <article className={`result-panel ${wide ? "wide" : ""}`}>
      <header>
        <span>{title}</span>
        <strong>{count}</strong>
      </header>
      <div className="panel-content">{children}</div>
    </article>
  );
}

function EmptyState({ text }) {
  return <p className="empty-state">{text}</p>;
}
