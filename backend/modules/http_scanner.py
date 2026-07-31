import requests


REQUEST_TIMEOUT = (3, 5)

USER_AGENT = (
    "VulnScanner/2.0 "
    "(Authorized Defensive Security Assessment)"
)


class HttpScanError(RuntimeError):
    """Raised when an unexpected HTTP scanning error occurs."""


def build_result(
    available=False,
    url=None,
    protocol=None,
    status_code=None,
    headers=None,
    error=None,
):
    """Create a consistent HTTP scan response."""

    return {
        "available": available,
        "url": url,
        "protocol": protocol,
        "status_code": status_code,
        "headers": headers or {},
        "error": error,
    }


def scan_http(target):
    """
    Inspect response headers using HTTPS first, then HTTP.

    Redirects are intentionally disabled to prevent a public target from
    redirecting the scanner toward a private or local address.
    """

    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
    }

    errors = []

    for scheme in ("https", "http"):
        url = f"{scheme}://{target}"

        try:
            with requests.get(
                url,
                headers=request_headers,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=False,
                verify=True,
                stream=True,
            ) as response:
                safe_headers = {
                    str(key): str(value)[:2000]
                    for key, value in response.headers.items()
                }

                return build_result(
                    available=True,
                    url=url,
                    protocol=scheme.upper(),
                    status_code=response.status_code,
                    headers=safe_headers,
                )

        except requests.exceptions.SSLError:
            errors.append(
                f"{scheme.upper()} certificate validation failed."
            )

        except requests.exceptions.Timeout:
            errors.append(
                f"{scheme.upper()} request timed out."
            )

        except requests.exceptions.ConnectionError:
            errors.append(
                f"{scheme.upper()} connection failed."
            )

        except requests.exceptions.RequestException:
            errors.append(
                f"{scheme.upper()} request could not be completed."
            )

    return build_result(
        error=" ".join(errors)
        or "No HTTP or HTTPS response was available."
    )