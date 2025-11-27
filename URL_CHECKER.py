#!/usr/bin/env python3
# url_check.py — Simple URL status & latency checker
import requests
import time
from pathlib import Path

TIMEOUT = 5

def check_url(url):
    try:
        start = time.time()
        r = requests.get(url, timeout=TIMEOUT)
        elapsed = (time.time() - start) * 1000.0
        return r.status_code, elapsed, None
    except Exception as e:
        return None, None, str(e)

def run_list(path_or_none=None):
    urls = []
    if path_or_none:
        p = Path(path_or_none)
        if p.exists():
            urls = [line.strip() for line in p.read_text().splitlines() if line.strip()]
    if not urls:
        # default examples
        urls = ["https://www.google.com", "https://httpbin.org/status/404", "https://example.com"]
    for u in urls:
        code, ms, err = check_url(u)
        if err:
            print(f"{u:40} ERROR -> {err}")
        else:
            print(f"{u:40} {code}  {ms:.0f} ms")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Check URL status codes and latency. Provide a file of URLs if desired.")
    p.add_argument("--file", "-f", help="Path to newline-separated file of URLs")
    args = p.parse_args()
    run_list(args.file)