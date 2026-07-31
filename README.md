VulnScanner

VulnScanner is a full-stack educational security assessment tool built with React and Flask. It checks a curated list of common TCP ports, reviews HTTP response headers, identifies selected exposed services, classifies risk, and provides concise AI-assisted recommendations.

Authorized use only: scan only systems you own or have explicit permission to assess. Results are educational indicators and must be verified manually.

Live demo

Frontend: vulnscanner-five.vercel.app

The frontend remains publicly accessible. Scanner functionality depends on the separate Flask backend being online and correctly configured.

Features

Common TCP port scanning using Python sockets

Service identification for detected ports

HTTP response-header inspection

Detection of selected risky exposed services

Low, medium, and high risk classification

Optional Gemini-generated security recommendations

Recent scan history in the browser session

Downloadable security report

Responsive React dashboard

Architecture

flowchart LR
U["User"] --> F["React frontend"]
F -->|POST /scan| B["Flask API"]
B --> T["Authorized target"]
B --> G["Gemini API"]
B -->|JSON result| F

Technology stack

Layer

Technology

Frontend

React, Vite, Axios, jsPDF

Backend

Python, Flask, Flask-CORS, Requests

Scanning

Python sockets and HTTP-header analysis

AI

Google GenAI SDK

Frontend hosting

Vercel

Project structure

vulnscanner/
├── backend/
│ ├── modules/
│ ├── templates/
│ ├── utils/
│ ├── app.py
│ ├── scanner.py
│ └── requirements.txt
├── frontend/
│ ├── public/
│ ├── src/
│ ├── package.json
│ └── vite.config.js
├── .env.example
├── .gitignore
└── README.md

Run locally

1. Backend

From the project root in Windows PowerShell:

py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:GEMINI_API_KEY="your_new_api_key"
$env:FLASK_DEBUG="false"
py backend\app.py

The backend runs at http://127.0.0.1:5000 by default.

2. Frontend

Open another terminal:

cd frontend
npm install
npm run dev

The frontend runs at http://localhost:5173.

Environment variables

GEMINI_API_KEY=replace_with_your_new_api_key
FLASK_DEBUG=false

Never commit a real .env file or API key. The committed .env.example file must contain placeholders only.

API

GET /

Checks whether the Flask backend is running.

POST /scan

Example request:

{
"target": "example.com"
}

The response contains the target, resolved IP address, detected open ports, HTTP headers, risk classification, selected findings, and security recommendations.

Limitations

Scans only a curated list of common ports

Does not perform exploitation or authenticated testing

Does not replace Nmap, a professional vulnerability scanner, or a penetration test

Risk classification is heuristic and requires manual verification

Public hosting providers may restrict outbound port connections

Roadmap

Deploy the Flask backend to a new hosting provider

Configure the frontend API URL through an environment variable

Add stricter target validation and private-IP protection

Add request rate limiting

Add automated frontend and backend tests

Improve report formatting and accessibility

Author

Developed by Nahnu Rohmania as a cybersecurity portfolio project.
