#!/usr/bin/env python3
"""Check common HTTP security headers on a website you are authorized to assess."""

import argparse
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SECURITY_HEADERS = {
    "content-security-policy": "Helps control which sources a browser may load content from.",
    "strict-transport-security": "Tells browsers to use HTTPS for future connections.",
    "x-content-type-options": "Helps prevent MIME-type sniffing.",
    "referrer-policy": "Controls how much referrer information browsers send.",
    "permissions-policy": "Controls access to selected browser features.",
    "x-frame-options": "Provides legacy protection against framing-based clickjacking.",
}


def normalize_url(raw_url):
    raw_url = raw_url.strip()
    if not raw_url:
        raise ValueError("URL cannot be empty.")
    if "://" not in raw_url:
        raw_url = "https://" + raw_url
    parsed = urlparse(raw_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter a valid http:// or https:// URL.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing embedded credentials are not supported.")
    return raw_url


def fetch_headers(url, timeout):
    request = Request(
        url,
        headers={"User-Agent": "HTTP-Security-Headers-Auditor/1.0"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.geturl(), response.status, response.headers
    except HTTPError as exc:
        # Error responses can still provide useful headers.
        return exc.geturl(), exc.code, exc.headers
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Request failed: {getattr(exc, 'reason', exc)}") from exc


def main():
    parser = argparse.ArgumentParser(
        description="Audit common HTTP security headers on an authorized website."
    )
    parser.add_argument("url", help="Website URL, e.g. https://example.com")
    parser.add_argument("--timeout", type=float, default=10,
                        help="Request timeout in seconds (default: 10)")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        url = normalize_url(args.url)
        final_url, status, headers = fetch_headers(url, args.timeout)
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("=" * 58)
    print("HTTP SECURITY HEADERS AUDITOR")
    print("=" * 58)
    print(f"Requested URL : {url}")
    print(f"Final URL     : {final_url}")
    print(f"HTTP status   : {status}")
    print("\nHeader review:")

    found = 0
    for name, purpose in SECURITY_HEADERS.items():
        value = headers.get(name)
        if value:
            found += 1
            print(f"\n[+] {name}: PRESENT")
            print(f"    Value: {value}")
        else:
            print(f"\n[-] {name}: NOT FOUND")
            print("    Suggestion: Review whether this header is appropriate")
            print("    for the application and configure it if needed.")
        print(f"    Purpose: {purpose}")

    print("\n" + "-" * 58)
    print(f"Headers found: {found}/{len(SECURITY_HEADERS)}")
    print("Note: Missing headers are review items, not proof of a vulnerability.")
    print("Header presence alone does not prove a website is secure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
