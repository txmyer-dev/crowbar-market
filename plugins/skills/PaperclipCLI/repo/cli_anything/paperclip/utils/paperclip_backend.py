"""Paperclip backend — HTTP client that talks to the running Paperclip server.

The Paperclip server is a HARD DEPENDENCY. If it is not reachable, every
operation will fail with a clear error message.
"""

import json
import os
import urllib.error
import urllib.request
from typing import Any


DEFAULT_URL = "http://localhost:3100"


class PaperclipError(Exception):
    """Raised when a Paperclip API call fails."""

    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


class PaperclipClient:
    """HTTP client for the Paperclip REST API.

    Uses only stdlib (urllib) — no external HTTP dependencies required.
    """

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = (
            base_url
            or os.environ.get("PAPERCLIP_URL")
            or DEFAULT_URL
        ).rstrip("/")
        self.api_key = api_key or os.environ.get("PAPERCLIP_API_KEY") or ""

    # ── Low-level request ─────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        params: dict | None = None,
    ) -> dict:
        """Send an HTTP request to the Paperclip API.

        Returns parsed JSON response body.  Raises *PaperclipError* on
        HTTP errors or connection failures.
        """
        url = f"{self.base_url}/api{path}"

        if params:
            qs = "&".join(
                f"{k}={urllib.request.quote(str(v))}"
                for k, v in params.items()
                if v is not None
            )
            if qs:
                url = f"{url}?{qs}"

        data = json.dumps(body).encode() if body is not None else None

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        run_id = os.environ.get("PAPERCLIP_RUN_ID")
        if run_id:
            headers["X-Paperclip-Run-Id"] = run_id

        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode()
                if not raw:
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as exc:
            raw_body = ""
            try:
                raw_body = exc.read().decode()
            except Exception:
                pass
            parsed = None
            try:
                parsed = json.loads(raw_body)
            except Exception:
                pass
            msg = f"HTTP {exc.code}"
            if parsed and isinstance(parsed, dict):
                msg = parsed.get("error", parsed.get("message", msg))
            raise PaperclipError(msg, status=exc.code, body=parsed) from exc
        except urllib.error.URLError as exc:
            raise PaperclipError(
                f"Cannot connect to Paperclip server at {self.base_url}.\n"
                f"  Ensure the server is running:\n"
                f"    cd <paperclip-dir> && pnpm dev\n"
                f"  Or set PAPERCLIP_URL to the correct address.\n"
                f"  Error: {exc.reason}"
            ) from exc

    # ── HTTP verb helpers ─────────────────────────────────────────────

    def get(self, path: str, params: dict | None = None) -> dict:
        return self._request("GET", path, params=params)

    def post(self, path: str, body: dict | None = None) -> dict:
        return self._request("POST", path, body=body or {})

    def patch(self, path: str, body: dict | None = None) -> dict:
        return self._request("PATCH", path, body=body or {})

    def put(self, path: str, body: dict | None = None) -> dict:
        return self._request("PUT", path, body=body or {})

    def delete(self, path: str) -> dict:
        return self._request("DELETE", path)

    # ── Convenience: health check ─────────────────────────────────────

    def health(self) -> dict:
        """Check server health. Returns the health JSON payload."""
        return self.get("/health")
