RISKY_SERVICES = {
    21: {
        "severity": "Medium",
        "issue": "FTP is reachable on the scanned network interface.",
        "recommendation": (
            "Replace FTP with SFTP or restrict access using firewall rules."
        ),
    },
    23: {
        "severity": "High",
        "issue": "Telnet is reachable and does not encrypt session traffic.",
        "recommendation": (
            "Disable Telnet and use SSH with strong authentication."
        ),
    },
    445: {
        "severity": "High",
        "issue": "SMB is reachable on the scanned network interface.",
        "recommendation": (
            "Restrict SMB to trusted internal networks and apply updates."
        ),
    },
    3306: {
        "severity": "High",
        "issue": "MySQL is reachable on the scanned network interface.",
        "recommendation": (
            "Restrict database access to trusted application servers."
        ),
    },
    3389: {
        "severity": "High",
        "issue": "Remote Desktop is reachable on the scanned network interface.",
        "recommendation": (
            "Place RDP behind a VPN and enforce MFA and account lockout."
        ),
    },
    5432: {
        "severity": "High",
        "issue": "PostgreSQL is reachable on the scanned network interface.",
        "recommendation": (
            "Restrict database access using firewall and network rules."
        ),
    },
}


SECURITY_HEADERS = {
    "content-security-policy": {
        "severity": "Medium",
        "issue": "Content-Security-Policy header is missing.",
        "recommendation": "Define a restrictive Content-Security-Policy.",
    },
    "strict-transport-security": {
        "severity": "Medium",
        "issue": "Strict-Transport-Security header is missing.",
        "recommendation": (
            "Enable HSTS after confirming the website fully supports HTTPS."
        ),
        "https_only": True,
    },
    "x-frame-options": {
        "severity": "Low",
        "issue": "X-Frame-Options header is missing.",
        "recommendation": "Use X-Frame-Options or CSP frame-ancestors.",
    },
    "x-content-type-options": {
        "severity": "Low",
        "issue": "X-Content-Type-Options header is missing.",
        "recommendation": "Set X-Content-Type-Options to nosniff.",
    },
    "referrer-policy": {
        "severity": "Low",
        "issue": "Referrer-Policy header is missing.",
        "recommendation": "Configure a restrictive Referrer-Policy.",
    },
}


SEVERITY_SCORES = {
    "Low": 1,
    "Medium": 2,
    "High": 5,
}


def create_finding(category, severity, issue, recommendation, port=None):
    """Return one normalized defensive security finding."""

    return {
        "category": category,
        "severity": severity,
        "port": port,
        "issue": issue,
        "recommendation": recommendation,
    }


def check_service_exposure(open_ports):
    """Match reachable services against the educational risk rules."""

    findings = []

    for service in open_ports:
        port = service.get("port")
        rule = RISKY_SERVICES.get(port)

        if rule is None:
            continue

        findings.append(
            create_finding(
                category="Reachable Service",
                severity=rule["severity"],
                port=port,
                issue=rule["issue"],
                recommendation=rule["recommendation"],
            )
        )

    return findings


def check_security_headers(http_result):
    """Report selected missing defensive HTTP response headers."""

    if not http_result.get("available"):
        return []

    response_headers = {
        str(key).lower(): value
        for key, value in http_result.get("headers", {}).items()
    }

    protocol = str(http_result.get("protocol") or "").lower()
    finding_port = 443 if protocol == "https" else 80
    findings = []

    for header_name, rule in SECURITY_HEADERS.items():
        if rule.get("https_only") and protocol != "https":
            continue

        if header_name in response_headers:
            continue

        findings.append(
            create_finding(
                category="Missing Security Header",
                severity=rule["severity"],
                port=finding_port,
                issue=rule["issue"],
                recommendation=rule["recommendation"],
            )
        )

    return findings


def calculate_risk(findings):
    """Calculate a transparent educational heuristic score."""

    score = sum(
        SEVERITY_SCORES.get(finding.get("severity"), 0)
        for finding in findings
    )

    if score >= 8:
        risk = "High"
    elif score >= 3:
        risk = "Medium"
    else:
        risk = "Low"

    return risk, score


def analyze_vulnerabilities(open_ports, http_result):
    """Analyze service exposure and HTTP-header signals."""

    findings = [
        *check_service_exposure(open_ports),
        *check_security_headers(http_result),
    ]

    risk, score = calculate_risk(findings)
    severity_count = {"High": 0, "Medium": 0, "Low": 0}

    for finding in findings:
        severity = finding.get("severity")

        if severity in severity_count:
            severity_count[severity] += 1

    return {
        "risk": risk,
        "score": score,
        "findings": findings,
        "severity_count": severity_count,
    }