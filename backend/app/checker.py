"""Website pinging utilities.

Provides an asynchronous `ping_url` function that measures HTTP status and response time.
Uses `httpx` for async HTTP requests.
"""
from __future__ import annotations

import time
from typing import Optional

import httpx


async def ping_url(url: str, timeout: float = 10.0) -> dict:
    """Ping `url` with an async HTTP GET and measure response time.

    Returns a dict with keys:
    - `url`: original URL
    - `status`: HTTP status code or None on error
    - `response_time_ms`: elapsed time in milliseconds (int)
    - `ok`: boolean (True for 2xx/3xx responses)
    - `error`: optional error message when the request failed

    Why async? Using an async client lets a scheduler run many pings concurrently
    without blocking threads. `httpx` supports both sync and async APIs; we
    choose the async API for scalability.
    """
    start = time.monotonic()
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(url, timeout=timeout)
        elapsed_ms = int((time.monotonic() - start) * 1000)
        status = resp.status_code
        return {
            "url": url,
            "status": status,
            "response_time_ms": elapsed_ms,
            "ok": 200 <= status < 400,
        }
    except httpx.RequestError as exc:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "url": url,
            "status": None,
            "response_time_ms": elapsed_ms,
            "ok": False,
            "error": str(exc),
        }
