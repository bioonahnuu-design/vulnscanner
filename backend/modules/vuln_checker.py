def check_vulnerabilities(headers):
    print("\n[+] Checking vulnerabilities...")
    print("-" * 40)

    if headers is None:
        print("No headers to analyze.")
        return

    security_headers = [
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Strict-Transport-Security"
    ]

    for header in security_headers:
        if header not in headers:
            print(f"[VULNERABLE] Missing {header}")
        else:
            print(f"[OK] {header} found")