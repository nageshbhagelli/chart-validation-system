"""
Utility / Helper Functions
===========================
Shared helpers used across the application.
"""

from datetime import datetime, timezone
from typing import Any, Dict


def timestamp_now() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def build_error_response(detail: str, status_code: int = 400) -> Dict[str, Any]:
    """
    Build a standardised error payload.

    Parameters
    ----------
    detail : str
        Human-readable error description.
    status_code : int
        HTTP status code (for logging; not set on the response itself).

    Returns
    -------
    dict with keys: error, detail, timestamp.
    """
    return {
        "error": True,
        "detail": detail,
        "timestamp": timestamp_now(),
    }
