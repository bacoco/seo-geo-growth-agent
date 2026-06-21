#!/usr/bin/env python3
"""Serve a generated SEO/GEO HTML report locally."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import socket
import webbrowser
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, type=Path, help="Report directory containing index.html.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host. Defaults to 127.0.0.1.")
    parser.add_argument("--port", default=8766, type=int, help="Preferred port. Use 0 for any free port.")
    parser.add_argument("--open", action="store_true", help="Open the report URL in the system browser.")
    parser.add_argument("--check", action="store_true", help="Validate the report directory and exit.")
    return parser.parse_args()


def validate_report_dir(path: Path) -> Path:
    report_dir = path.resolve()
    index = report_dir / "index.html"
    if not report_dir.is_dir():
        raise SystemExit(f"Report directory does not exist: {report_dir}")
    if not index.is_file():
        raise SystemExit(f"Report directory is missing index.html: {index}")
    return report_dir


def port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex((host, port)) != 0


def choose_port(host: str, preferred: int) -> int:
    if preferred == 0:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, 0))
            return int(sock.getsockname()[1])
    if port_available(host, preferred):
        return preferred
    for port in range(preferred + 1, preferred + 100):
        if port_available(host, port):
            return port
    raise SystemExit(f"No free port found near {preferred}")


def update_receipt(report_dir: Path, url: str) -> None:
    audit_path = report_dir / "audit.json"
    receipt_path = report_dir / "LATEST-SEO-GEO-REPORT.md"
    if not audit_path.is_file():
        return
    try:
        audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    summary = audit.get("summary") if isinstance(audit.get("summary"), dict) else {}
    context = audit.get("context") if isinstance(audit.get("context"), dict) else {}
    ai_layer = audit.get("ai_layer_package") if isinstance(audit.get("ai_layer_package"), dict) else {}
    lines = [
        "# Latest SEO/GEO Report",
        "",
        f"- Site: {audit.get('site', 'unknown')}",
        f"- Audited URL: {audit.get('audited_url') or audit.get('url') or audit.get('site', 'unknown')}",
        f"- Generated at: {audit.get('generated_at', 'unknown')}",
        f"- Environment: {audit.get('environment') or context.get('environment') or 'unknown'}",
        f"- HTML path: {report_dir / 'index.html'}",
        f"- Audit JSON: {audit_path}",
        f"- Local URL: {url}",
        f"- Summary: {summary.get('headline', 'unknown')}",
        f"- Screenshot status: {audit.get('screenshot_status', 'see audit.json')}",
        f"- AI layer package: {ai_layer.get('zip_path', 'not generated')}",
        "",
    ]
    receipt_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    report_dir = validate_report_dir(args.dir)
    if args.check:
        print(f"Report directory OK: {report_dir}")
        return

    port = choose_port(args.host, args.port)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(report_dir))
    server = http.server.ThreadingHTTPServer((args.host, port), handler)
    url = f"http://{args.host}:{port}/"
    update_receipt(report_dir, url)
    print(f"Serving report: {url}")
    print("Press Ctrl-C to stop.")
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
