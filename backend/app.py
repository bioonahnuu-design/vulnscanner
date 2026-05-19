from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import requests
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# GEMINI SETUP
client = genai.Client(
    api_key="AIzaSyBd76gKZDWOLkj9wXQ5UIU3Xz_eaJhgg_o"
)

COMMON_PORTS = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    135: "rpc",
    139: "netbios",
    143: "imap",
    443: "https",
    445: "smb",
    3306: "mysql",
    3389: "rdp",
    8080: "http-proxy"
}


def detect_risk(open_ports_count):

    if open_ports_count >= 8:
        return "High"

    elif open_ports_count >= 4:
        return "Medium"

    else:
        return "Low"


@app.route("/")
def home():

    return jsonify({
        "message": "VulnScanner Backend Running"
    })


@app.route("/scan", methods=["POST"])
def scan_target():

    print("SCAN HIT")

    try:

        data = request.get_json()

        print(data)

        if not data:
            return jsonify({
                "error": "No data received"
            }), 400

        target = data.get("target")

        if not target:
            return jsonify({
                "error": "No target provided"
            }), 400

        # CLEAN TARGET
        target = target.strip()
        target = target.replace("http://", "")
        target = target.replace("https://", "")
        target = target.split("/")[0]

        # GET IP
        try:

            ip = socket.gethostbyname(target)

        except Exception:

            return jsonify({
                "error": "Invalid hostname"
            }), 400

        # OPEN PORTS
        ports_data = []

        for port, service in COMMON_PORTS.items():

            try:

                s = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                s.settimeout(0.5)

                result = s.connect_ex((ip, port))

                if result == 0:

                    ports_data.append({
                        "port": port,
                        "service": service
                    })

                s.close()

            except Exception:
                pass

        # HTTP HEADERS
        headers = {}

        try:

            url = f"http://{target}"

            response = requests.get(
                url,
                timeout=3,
                verify=False
            )

            headers = dict(response.headers)

        except Exception:

            headers = {
                "Server": "Unknown",
                "Connection": "Unknown"
            }

        # VULNERABILITIES
        vulnerabilities = []

        risky_ports = {
            21: "FTP exposed",
            23: "Telnet insecure protocol",
            445: "SMB exposure",
            3389: "RDP exposed"
        }

        for item in ports_data:

            port = item["port"]

            if port in risky_ports:

                vulnerabilities.append({
                    "port": port,
                    "issue": risky_ports[port]
                })

        # RISK
        risk = detect_risk(len(ports_data))

        # AI ANALYSIS
        prompt = f"""

Analyze this cybersecurity scan briefly.

Open Ports:
{ports_data}

Risk Level:
{risk}

Give:
- possible risks
- short recommendations

Maximum 3 bullet points.
"""

        try:

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            ai_analysis = response.text

        except Exception:

            ai_analysis = (
                "• Several ports are publicly accessible.\n\n"
                "• Open ports may increase attack surface.\n\n"
                "• Ensure firewall protection is enabled.\n\n"
                "• Disable unused services if possible.\n\n"
                "• Use strong authentication for exposed services."
            )

        return jsonify({
            "target": target,
            "ip": ip,
            "risk": risk,
            "ports": ports_data,
            "headers": headers,
            "vulnerabilities": vulnerabilities,
            "ai_analysis": ai_analysis
        })

    except Exception as e:

        print("BACKEND ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )