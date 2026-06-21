#!/usr/bin/env python3
"""Shared runtime constants and safety helpers for seo-geo-growth-agent scripts."""
from __future__ import annotations

import ipaddress
import shutil
from pathlib import Path
from urllib.parse import urlparse

VERSION = "1.3.2"
USER_AGENT = f"seo-geo-growth-agent/{VERSION}"


def normalize_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        raise ValueError("URL is required")
    parsed = urlparse(value)
    if parsed.scheme:
        return value
    return f"https://{value}"


def is_local_hostname(hostname: str) -> bool:
    host = (hostname or "").strip().strip("[]").rstrip(".").lower()
    if not host:
        return False
    if host == "localhost" or host.endswith(".localhost"):
        return True
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(
        (
            address.is_loopback,
            address.is_private,
            address.is_link_local,
            address.is_unspecified,
            address.is_reserved,
            address.is_multicast,
        )
    )


def validate_network_url(url: str, *, allow_local: bool = False) -> str:
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only http:// and https:// URLs are supported for network access.")
    if not parsed.netloc or not parsed.hostname:
        raise ValueError(f"invalid URL: {url}")
    if is_local_hostname(parsed.hostname) and not allow_local:
        raise ValueError(
            "Local, private, reserved, and loopback targets require explicit --allow-local."
        )
    return normalized


def clean_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
