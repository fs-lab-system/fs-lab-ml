import json
import os
from typing import Any, Dict

from src.api_response import api_success, api_error
from src.config import RAW_DATA_DIR, RAW_DATA_FILE


def _describe(value: Any) -> Dict[str, Any]:
    return {
        "type": type(value).__name__,
        "is_null": value is None,
        "is_empty": value == {} or value == [] or value == "",
    }


def inspect_raw_data():
    path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)

   # error warning
    if not os.path.exists(path):
        return api_error(
            code="RAW_DATA_NOT_FOUND",
            message=f"File not found: {path}",
        )

   # read-only data access
    with open( path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary: Dict[str, Any] = {
        "root_type": type(data).__name__,
               }

    # object (dict)
    if isinstance(data, dict):
        summary["keys"] = {
            key: _describe(value) for key, value in data.items()
        }

    # list
    elif isinstance(data, list):
        summary["length"] = len(data)
        if data:
            summary["first_item_type"] = type(data[0]).__name__

    return api_success(summary)
