import shutil
from pathlib import Path

import nmap


TARGET_PORTS = (
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    135,
    139,
    143,
    443,
    445,
    3306,
    3389,
    5432,
    8080,
)

NMAP_ARGUMENTS = (
    "-Pn "
    "-sT "
    "-sV "
    "--version-light "
    "-T4 "
    "--max-retries 1 "
    "--host-timeout 25s"
)


class PortScanError(RuntimeError):
    """Raised when Nmap cannot complete the port scan."""


def find_nmap():
    """
    Locate the Nmap executable without relying on one hardcoded path.
    """

    detected_path = shutil.which("nmap")

    if detected_path:
        return detected_path

    windows_locations = (
        Path(r"C:\Program Files\Nmap\nmap.exe"),
        Path(r"C:\Program Files (x86)\Nmap\nmap.exe"),
    )

    for location in windows_locations:
        if location.exists():
            return str(location)

    raise PortScanError(
        "Nmap is not installed or is not available through PATH."
    )


def build_version(service_data):
    """
    Combine Nmap product, version, and extra information into one label.
    """

    version_parts = [
        service_data.get("product", ""),
        service_data.get("version", ""),
        service_data.get("extrainfo", ""),
    ]

    return " ".join(
        part.strip()
        for part in version_parts
        if part and part.strip()
    )


def scan_ports(ip_address):
    """
    Scan a curated list of common TCP ports.

    The target must already be validated before this function is called.
    """

    nmap_path = find_nmap()

    try:
        scanner = nmap.PortScanner(
            nmap_search_path=(nmap_path,)
        )

        scanner.scan(
            hosts=ip_address,
            ports=",".join(str(port) for port in TARGET_PORTS),
            arguments=NMAP_ARGUMENTS,
        )

    except nmap.PortScannerError as error:
        raise PortScanError(
            f"Nmap could not start: {error}"
        ) from error

    except Exception as error:
        raise PortScanError(
            "Unexpected error while running Nmap."
        ) from error

    available_hosts = scanner.all_hosts()

    if not available_hosts:
        return []

    host = (
        ip_address
        if ip_address in available_hosts
        else available_hosts[0]
    )

    if "tcp" not in scanner[host]:
        return []

    results = []

    for port, service_data in scanner[host]["tcp"].items():
        if service_data.get("state") != "open":
            continue

        service_name = service_data.get("name") or "unknown"
        version = build_version(service_data)

        results.append(
            {
                "port": int(port),
                "protocol": "tcp",
                "state": "open",
                "service": service_name,
                "version": version or "unknown",
            }
        )

    return sorted(
        results,
        key=lambda item: item["port"],
    )