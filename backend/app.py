import logging
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai

try:
    from .modules.http_scanner import scan_http
    from .modules.port_scanner import PortScanError, scan_ports
    from .modules.target_validator import TargetValidationError, validate_target
    from .modules.vuln_checker import analyze_vulnerabilities
except ImportError:
    from modules.http_scanner import scan_http
    from modules.port_scanner import PortScanError, scan_ports
    from modules.target_validator import TargetValidationError, validate_target
    from modules.vuln_checker import analyze_vulnerabilities


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096


def get_allowed_origins():
    configured_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )

    return [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


CORS(
    app,
    resources={
        r"/scan": {
            "origins": get_allowed_origins(),
            "methods": ["POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        },
        r"/health": {
            "origins": get_allowed_origins(),
            "methods": ["GET"],
        },
    },
)

gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

gemini_client = (
    genai.Client(api_key=gemini_api_key)
    if gemini_api_key
    else None
)


def build_fallback_analysis(findings):
    recommendations = []

    for finding in findings:
        recommendation = finding.get("recommendation")

        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

        if len(recommendations) == 3:
            break

    default_recommendations = [
        "Restrict unnecessary services to trusted network sources.",
        "Keep exposed services patched and monitor their access logs.",
        "Verify these heuristic findings through an authorized manual review.",
    ]

    for recommendation in default_recommendations:
        if recommendation not in recommendations:
            recommendations.append(recommendation)

        if len(recommendations) == 3:
            break

    return "\n".join(
        f"• {recommendation}"
        for recommendation in recommendations
    )


def generate_ai_analysis(target, ports, risk, findings):
    fallback = build_fallback_analysis(findings)

    if gemini_client is None:
        return fallback, "fallback"

    compact_ports = [
        {
            "port": item.get("port"),
            "service": item.get("service"),
        }
        for item in ports
    ]

    compact_findings = [
        {
            "severity": item.get("severity"),
            "issue": item.get("issue"),
        }
        for item in findings[:10]
    ]

    prompt = f"""
You are assisting with an authorized defensive security assessment.

Target hostname: {target}
Detected services: {compact_ports}
Risk classification: {risk}
Findings: {compact_findings}

Give exactly three concise defensive recommendations.
Do not provide exploitation instructions.
"""

    try:
        response = gemini_client.models.generate_content(
            model=gemini_model,
            contents=prompt,
        )

        generated_text = getattr(response, "text", "").strip()

        if generated_text:
            return generated_text, "gemini"

        return fallback, "fallback"

    except Exception as error:
        logger.warning(
            "Gemini analysis unavailable: %s",
            type(error).__name__,
        )
        return fallback, "fallback"


@app.get("/")
def home():
    return jsonify(
        {
            "name": "VulnScanner API",
            "status": "running",
            "authorized_use_only": True,
            "ai_configured": gemini_client is not None,
            "ai_model": gemini_model if gemini_client is not None else None,
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "ai_configured": gemini_client is not None,
        }
    )


@app.post("/scan")
def scan_target():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    raw_target = data.get("target", "")

    try:
        target, ip_address = validate_target(raw_target)

        open_ports = scan_ports(ip_address)
        http_result = scan_http(target)
        analysis = analyze_vulnerabilities(open_ports, http_result)

        ai_analysis, analysis_source = generate_ai_analysis(
            target=target,
            ports=open_ports,
            risk=analysis["risk"],
            findings=analysis["findings"],
        )

        return jsonify(
            {
                "target": target,
                "ip": ip_address,
                "risk": analysis["risk"],
                "risk_score": analysis["score"],
                "ports": open_ports,
                "headers": http_result.get("headers", {}),
                "http": {
                    "available": http_result.get("available", False),
                    "url": http_result.get("url"),
                    "protocol": http_result.get("protocol"),
                    "status_code": http_result.get("status_code"),
                    "error": http_result.get("error"),
                },
                "vulnerabilities": analysis["findings"],
                "severity_count": analysis["severity_count"],
                "ai_analysis": ai_analysis,
                "analysis_source": analysis_source,
            }
        )

    except TargetValidationError as error:
        return jsonify({"error": str(error)}), 400

    except PortScanError as error:
        logger.warning("Port scan failed: %s", error)
        return jsonify(
            {
                "error": (
                    "Port scanner is unavailable. "
                    "Check the Nmap installation."
                )
            }
        ), 503

    except Exception:
        logger.exception("Unexpected scan error")
        return jsonify(
            {"error": "An unexpected server error occurred."}
        ), 500


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large."}), 413


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )