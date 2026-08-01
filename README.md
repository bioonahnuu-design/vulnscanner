<p align="center">
  <img src="docs/assets/vulnscanner-banner.svg" width="100%" alt="VulnScanner — Nahnu Security Lab" />
</p>

<h1 align="center">VulnScanner v2</h1>

<p align="center">
  <b>Surface the ports. Explain the risk.</b><br>
  An AI-assisted network exposure dashboard for authorized defensive assessments.
</p>

<p align="center">
  <a href="https://vulnscanner-five.vercel.app"><img src="https://img.shields.io/badge/LIVE_DEMO-16A36A?style=for-the-badge&logo=vercel&logoColor=white" alt="Live demo"></a>
  <a href="https://github.com/bioonahnuu-design/vulnscanner"><img src="https://img.shields.io/badge/SOURCE_CODE-101418?style=for-the-badge&logo=github&logoColor=white" alt="Source code"></a>
  <img src="https://img.shields.io/badge/STATUS-ACTIVE-62F2B2?style=for-the-badge&labelColor=102019" alt="Status active">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React_19-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Vite_8-646CFF?style=flat-square&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Nmap-004170?style=flat-square&logo=linux&logoColor=white" alt="Nmap">
  <img src="https://img.shields.io/badge/Gemini-4285F4?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini">
</p>

[!CAUTION]Authorized use only. Scan only infrastructure you own or have explicit permission to assess. A risk result is an educational heuristic—not proof that a system has been compromised.

🖥️ Interface Preview

<p align="center">
  <img src="docs/screenshots/dashboard-overview.png" width="100%" alt="VulnScanner dashboard overview" />
</p>

<table>
  <tr>
    <th width="50%">Assessment Summary</th>
    <th width="50%">Exposure & Remediation</th>
  </tr>
  <tr>
    <td><img src="docs/screenshots/assessment-result.png" alt="Assessment summary"></td>
    <td><img src="docs/screenshots/exposure-report.png" alt="Exposure report"></td>
  </tr>
</table>

⚡ Security Assessment Modules

<table>
  <tr>
    <th>Module</th>
    <th>Purpose</th>
    <th>Evidence Produced</th>
  </tr>
  <tr>
    <td>🔎 <b>Target Validator</b></td>
    <td>Normalizes input, resolves IPv4, and rejects malformed targets</td>
    <td>Validated hostname and resolved address</td>
  </tr>
  <tr>
    <td>📡 <b>Nmap Engine</b></td>
    <td>Runs bounded TCP service and lightweight version discovery</td>
    <td>Port, protocol, state, service, and version</td>
  </tr>
  <tr>
    <td>🌐 <b>HTTP Review</b></td>
    <td>Attempts HTTPS first and inspects observable response headers</td>
    <td>Protocol, status code, availability, and headers</td>
  </tr>
  <tr>
    <td>🚨 <b>Risk Engine</b></td>
    <td>Maps exposed services and missing headers to explainable findings</td>
    <td>Severity count, findings, and heuristic score</td>
  </tr>
  <tr>
    <td>🤖 <b>Gemini Brief</b></td>
    <td>Generates concise defensive remediation guidance</td>
    <td>Three recommendations with transparent source label</td>
  </tr>
  <tr>
    <td>🧰 <b>Local Fallback</b></td>
    <td>Keeps analysis usable when Gemini is unavailable</td>
    <td>Deterministic rule-based recommendations</td>
  </tr>
</table>

🔁 Assessment Pipeline

flowchart LR
A[Authorized Operator] --> B[React Dashboard]
B -->|POST /scan| C[Flask API]
C --> D[Target Validator]
D --> E[Nmap Discovery]
D --> F[HTTPS / HTTP Probe]
E --> G[Risk Engine]
F --> G
G --> H{Gemini configured?}
H -->|Yes| I[Gemini Brief]
H -->|No| J[Local Fallback]
I --> K[Exposure Report]
J --> K
K --> B

<table>
  <tr>
    <td align="center"><sub>ENGINE</sub><br><b>NMAP 7.x</b></td>
    <td align="center"><sub>SCAN MODE</sub><br><b>BOUNDED</b></td>
    <td align="center"><sub>RISK MODEL</sub><br><b>HEURISTIC</b></td>
    <td align="center"><sub>AI SOURCE</sub><br><b>TRANSPARENT</b></td>
    <td align="center"><sub>POLICY</sub><br><b>AUTHORIZED</b></td>
  </tr>
</table>

🧰 Technology Stack

Frontend

<p>
  <img src="https://img.shields.io/badge/REACT_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React 19">
  <img src="https://img.shields.io/badge/VITE_8-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite 8">
  <img src="https://img.shields.io/badge/RESPONSIVE_CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
</p>

Backend & Analysis

<p>
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FLASK-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/NMAP-004170?style=for-the-badge&logo=linux&logoColor=white" alt="Nmap">
  <img src="https://img.shields.io/badge/GOOGLE_GEMINI-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini">
</p>

Quality & Delivery

<p>
  <img src="https://img.shields.io/badge/ESLINT-4B32C3?style=for-the-badge&logo=eslint&logoColor=white" alt="ESLint">
  <img src="https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  <img src="https://img.shields.io/badge/VERCEL-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
</p>

📊 Transparent Risk Model

<table>
  <tr>
    <th>Severity</th>
    <th>Weight</th>
    <th>Example Signal</th>
  </tr>
  <tr>
    <td>🟢 <b>Low</b></td>
    <td><code>1</code></td>
    <td>Missing X-Frame-Options or Referrer-Policy</td>
  </tr>
  <tr>
    <td>🟡 <b>Medium</b></td>
    <td><code>2</code></td>
    <td>FTP reachable or missing Content-Security-Policy</td>
  </tr>
  <tr>
    <td>🔴 <b>High</b></td>
    <td><code>5</code></td>
    <td>Telnet, SMB, database, or RDP reachable</td>
  </tr>
</table>

Total Score

Dashboard Classification

0–2

Low

3–7

Medium

8+

High

[!IMPORTANT]The score communicates observable exposure signals. Reachability does not automatically mean public exposure, exploitation, or compromise.

🤖 Gemini AI with Honest Fallback

Analysis Source

Dashboard Label

Behaviour

Gemini API available

GEMINI GENERATED

Generates exactly three concise defensive recommendations

Key missing or provider unavailable

LOCAL FALLBACK

Uses deterministic recommendations from local security rules

Only compact defensive context is sent to Gemini: the normalized target, detected services, risk classification, and finding summaries. The prompt explicitly excludes exploitation guidance.

🔐 Defensive Controls

Control

Implementation

✅ Authorization gate

Operator must confirm ownership or explicit permission

✅ Target normalization

Rejects credentials, spaces, custom ports, and malformed input

✅ Private-target policy

Private targets are blocked unless deliberately enabled for an owned lab

✅ DNS rebinding reduction

Nmap receives the already validated IP address

✅ Bounded scan

Curated ports, limited retries, and a host timeout

✅ Secret isolation

Gemini credentials are loaded from backend environment variables

✅ Restricted CORS

Permitted frontend origins come from CORS_ORIGINS

✅ Safe error responses

Internal exceptions remain in backend logs

🚀 Quick Start

<details>
<summary><b>1 — Requirements and environment variables</b></summary>

Python 3.11 or newer

Node.js and npm

Nmap installed and available in PATH

Gemini API key (optional)

GEMINI_API_KEY=replace_with_your_key
GEMINI_MODEL=gemini-2.5-flash
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ALLOW_PRIVATE_TARGETS=true
FLASK_DEBUG=false
PORT=5000

ALLOW_PRIVATE_TARGETS=true should only be used for a lab you own.

</details>

<details>
<summary><b>2 — Start the Flask backend</b></summary>

git clone https://github.com/bioonahnuu-design/vulnscanner.git
cd vulnscanner

py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r .\backend\requirements.txt
python .\backend\app.py

Health check:

Invoke-RestMethod http://127.0.0.1:5000/health

</details>

<details>
<summary><b>3 — Start the React frontend</b></summary>

cd frontend
Copy-Item .env.example .env
npm install
npm run dev

Open http://localhost:5173.

</details>

📡 Nmap Profile

nmap -Pn -sT -sV --version-light -T4 --max-retries 1 --host-timeout 25s <target>

Option

Purpose

-Pn

Continue when ICMP discovery is filtered

-sT

Use a TCP connect scan without raw-packet privileges

-sV --version-light

Add lightweight service-version context

-T4

Use a faster timing profile for a controlled assessment

--max-retries 1

Keep repeated probes bounded

--host-timeout 25s

Prevent a scan from hanging the API

<details>
<summary><b>View the curated TCP port profile</b></summary>

21 FTP 22 SSH 23 Telnet 25 SMTP
53 DNS 80 HTTP 110 POP3 135 MSRPC
139 NetBIOS 143 IMAP 443 HTTPS 445 SMB
3306 MySQL 3389 RDP 5432 PostgreSQL
8080 HTTP Proxy

</details>

📁 Project Structure

vulnscanner/
├── backend/
│ ├── modules/
│ │ ├── http_scanner.py
│ │ ├── port_scanner.py
│ │ ├── target_validator.py
│ │ └── vuln_checker.py
│ ├── app.py
│ ├── scanner.py
│ └── requirements.txt
├── frontend/
│ ├── src/
│ ├── .env.example
│ ├── package.json
│ └── vite.config.js
├── docs/
│ ├── assets/
│ └── screenshots/
├── .env.example
├── .gitignore
└── README.md

🔌 API Contract

<details>
<summary><b>GET /health</b></summary>

GET /health

{
"status": "healthy"
}

</details>

<details>
<summary><b>POST /scan</b></summary>

POST /scan
Content-Type: application/json

{
"target": "127.0.0.1"
}

The response includes the resolved IP, detected ports, HTTP evidence, findings, severity counts, risk score, remediation brief, and analysis_source.

</details>

✅ Validation

Check

Result

Python module compilation

✅ PASS

ESLint

✅ PASS

Vite production build

✅ PASS

Authorized local assessment against 127.0.0.1

✅ PASS

py -m py_compile .\backend\app.py .\backend\modules\target_validator.py .\backend\modules\port_scanner.py .\backend\modules\http_scanner.py .\backend\modules\vuln_checker.py

cd frontend
npm run lint
npm run build

🗺️ Roadmap

React operator dashboard

Targeted Nmap service discovery

HTTPS-first header review

Explainable risk scoring

Gemini remediation with local fallback

Input validation and controlled private-target policy

Persistent scan history with privacy-aware retention

Configurable authorized port profiles

Rate limiting and production observability

Automated backend and frontend test suite

Signed report metadata and accessibility improvements

Nmap-capable backend deployment in a controlled environment

☁️ Deployment

Component

Status

Notes

React dashboard

🟢 Online

Hosted on Vercel

Flask + Nmap API

🟡 Local / redeploy

Requires an Nmap-capable runtime

Gemini analysis

🔵 Optional

Enabled through backend environment variables

The public interface may remain online while scanning is unavailable when the separate backend is offline.

<p align="center">
  <b>NAHNU SECURITY LAB / TOOL 02</b><br>
  Designed and engineered by <a href="https://github.com/bioonahnuu-design"><b>Nahnu Rohmania</b></a><br>
  Informatics Engineering · Universitas 17 Agustus 1945 Surabaya
</p>

<p align="center">
  <a href="https://github.com/bioonahnuu-design"><img src="https://img.shields.io/badge/GITHUB-bioonahnuu--design-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="mailto:bioonahnuu@gmail.com"><img src="https://img.shields.io/badge/EMAIL-CONTACT-16A36A?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>

<p align="center"><code>EDUCATIONAL</code> · <code>DEFENSIVE</code> · <code>AUTHORIZED</code></p>
