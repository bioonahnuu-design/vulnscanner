import requests

def scan_http(target):
    print(f"\n[+] Checking HTTP for: {target}")
    print("-" * 40)

    if not target.startswith("http"):
        target = "http://" + target

    try:
        response = requests.get(target, timeout=5)

        print(f"[STATUS] {response.status_code}")
        print("\n[HEADERS]")

        for key, value in response.headers.items():
            print(f"{key}: {value}")

        return response.headers

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return None