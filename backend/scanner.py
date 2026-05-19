from backend.modules.port_scanner import scan_ports
from backend.modules.http_scanner import scan_http
from backend.modules.vuln_checker import check_vulnerabilities
from utils.banner import show_banner

from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

import argparse
import json

init(autoreset=True)


def scan_target(target):
    open_ports = scan_ports(target)
    headers = scan_http(target)
    check_vulnerabilities(headers)

    return {
        "target": target,
        "open_ports": open_ports,
        "headers": dict(headers) if headers else {}
    }


def generate_html_report(data, filename="report.html"):
    html_content = """
    <html>
    <head>
        <title>Vulnerability Report</title>
        <style>
            body { font-family: Arial; background: #0f172a; color: #e2e8f0; }
            h1 { color: #38bdf8; }
            .card {
                background: #1e293b;
                padding: 15px;
                margin: 10px;
                border-radius: 10px;
            }
            .open { color: #22c55e; }
        </style>
    </head>
    <body>
        <h1>🔐 Vulnerability Scan Report</h1>
    """

    for item in data:
        html_content += f"""
        <div class="card">
            <h2>Target: {item['target']}</h2>
            <p><b>Open Ports:</b></p>
            <ul>
        """

        # 🔥 LOOP SERVICE DETECTION
        for p in item["open_ports"]:
            html_content += f"<li class='open'>{p['port']} ({p['service']})</li>"

        html_content += "<p><b>Headers:</b></p><ul>"

        for k, v in item["headers"].items():
            html_content += f"<li>{k}: {v}</li>"

        html_content += """
            </ul>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


def main():
    show_banner()

    parser = argparse.ArgumentParser(description="Mini Vulnerability Scanner")
    parser.add_argument("-t", "--targets", nargs="+", required=True)
    parser.add_argument("-o", "--output", default="report.json")

    args = parser.parse_args()
    targets = args.targets
    output_file = args.output

    results = []

    print(Fore.YELLOW + f"[+] Scanning {len(targets)} targets...\n")

    # ⚡ THREAD POOL (UBAH DISINI KALAU MAU CEPAT)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan_target, t) for t in targets]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Scanning Progress"):
            results.append(future.result())

    # 💾 SAVE JSON
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    # 🌐 SAVE HTML
    generate_html_report(results)

    print(Fore.GREEN + "\n[+] Scan Completed!")
    print(Fore.CYAN + f"[+] Report saved as {output_file} & report.html")


if __name__ == "__main__":
    main()