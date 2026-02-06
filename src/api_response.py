# API - first architecture

from datetime import datetime, timezone
from typing import Any, Dict, Optional

def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def api_success(
    data: Any,
    service: str = "fs-lab-ml",
    version: str = "0.1.0",
) -> Dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "error": None,
        "meta": {
            "service": service,
            "version": version,
            "timestamp": _timestamp(),
        },
    }


def api_error(
    code: str,
    message: str,
    service: str = "fs-lab-ml",
    version: str = "0.1.0",
) -> Dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
        },
        "meta": {
            "service": service,
            "version": version,
            "timestamp": _timestamp(),
        },
    }