"""Session management — persists CLI state between invocations."""

import json
import os
from pathlib import Path
from typing import Any

from cli_anything.paperclip.utils.paperclip_backend import PaperclipClient


DEFAULT_SESSION_DIR = Path.home() / ".cli-anything-paperclip"
SESSION_FILE = "session.json"


def _session_path(session_dir: str | Path | None = None) -> Path:
    d = Path(session_dir) if session_dir else DEFAULT_SESSION_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d / SESSION_FILE


def load_session(session_dir: str | Path | None = None) -> dict[str, Any]:
    """Load session state from disk. Returns empty dict if none exists."""
    p = _session_path(session_dir)
    if p.exists():
        return json.loads(p.read_text())
    return {}


def save_session(data: dict[str, Any], session_dir: str | Path | None = None) -> Path:
    """Save session state to disk. Returns the path written."""
    p = _session_path(session_dir)
    p.write_text(json.dumps(data, indent=2))
    return p


def clear_session(session_dir: str | Path | None = None) -> None:
    """Remove the session file."""
    p = _session_path(session_dir)
    if p.exists():
        p.unlink()


class Session:
    """Stateful session wrapping a PaperclipClient + persisted context."""

    def __init__(
        self,
        url: str | None = None,
        api_key: str | None = None,
        company_id: str | None = None,
        session_dir: str | Path | None = None,
    ):
        saved = load_session(session_dir)
        self.url = url or saved.get("url") or os.environ.get("PAPERCLIP_URL") or "http://localhost:3100"
        self.api_key = api_key or saved.get("api_key") or os.environ.get("PAPERCLIP_API_KEY") or ""
        self.company_id = company_id or saved.get("company_id") or os.environ.get("PAPERCLIP_COMPANY_ID") or ""
        self._session_dir = session_dir
        self.client = PaperclipClient(base_url=self.url, api_key=self.api_key)
        self._modified = False

    @property
    def has_company(self) -> bool:
        return bool(self.company_id)

    def require_company(self) -> str:
        """Return company_id or raise."""
        if not self.company_id:
            raise ValueError(
                "No company selected. Use 'company use <id>' or set PAPERCLIP_COMPANY_ID."
            )
        return self.company_id

    def set_company(self, company_id: str) -> None:
        self.company_id = company_id
        self._modified = True

    def save(self) -> Path:
        data = {
            "url": self.url,
            "api_key": self.api_key,
            "company_id": self.company_id,
        }
        return save_session(data, self._session_dir)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "company_id": self.company_id,
            "has_api_key": bool(self.api_key),
        }
