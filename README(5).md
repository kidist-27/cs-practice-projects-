# HTTP Security Headers Auditor

A Python command-line tool that checks a website's HTTP response for six common security-related headers and explains their purpose.

> **Responsible use:** Run this tool only against websites you own or are authorized to assess. It sends one ordinary HTTP GET request and does not exploit vulnerabilities.

## Features

- Accepts a URL with or without `https://`.
- Checks six common security headers.
- Displays the HTTP status and final URL after redirects.
- Explains the purpose of each header and flags headers not found.
- Supports a configurable request timeout.
- Uses only Python's standard library; no third-party packages are needed.

## Headers checked

| Header | Purpose |
|---|---|
| `Content-Security-Policy` | Helps restrict sources for browser-loaded content. |
| `Strict-Transport-Security` | Instructs browsers to use HTTPS for future connections. |
| `X-Content-Type-Options` | Helps prevent MIME-type sniffing. |
| `Referrer-Policy` | Controls referrer information sent by browsers. |
| `Permissions-Policy` | Controls access to selected browser features. |
| `X-Frame-Options` | Provides legacy framing protection; CSP `frame-ancestors` is a modern alternative. |

## Requirements

- Python 3.9 or later recommended.
- Internet access to reach the target website.
- No external dependencies.

## Usage

```bash
python3 security_headers_auditor.py https://example.com
```

A hostname without a scheme defaults to HTTPS:

```bash
python3 security_headers_auditor.py example.com
```

Set a custom timeout:

```bash
python3 security_headers_auditor.py https://example.com --timeout 15
```

## Example output

Results depend on the website. This is illustrative output, not a live assessment:

```text
HTTP SECURITY HEADERS AUDITOR
Requested URL : https://example.com
HTTP status   : 200

[+] x-content-type-options: PRESENT
    Value: nosniff

[-] content-security-policy: NOT FOUND
    Suggestion: Review whether this header is appropriate.
```

## Project structure

```text
http-security-auditor/
├── security_headers_auditor.py
└── README.md
```

## Limitations

- A header may be present but configured incorrectly.
- A missing header is not automatically a vulnerability; context matters.
- This tool does not crawl the site, test application logic, or assess every web vulnerability.
- Some websites may block automated requests or return different headers on different routes.
- It checks the response from one GET request only.

## Learning objectives

Practice Python functions, dictionaries, command-line arguments, HTTP requests, URL parsing, exception handling, and introductory web security concepts.

## Future improvements

- Add unit tests.
- Export findings as JSON.
- Support a list of authorized URLs.
- Add carefully documented guidance for interpreting header configurations.

## Disclaimer

For educational use and authorized defensive assessment. Review findings in context before making security decisions.
