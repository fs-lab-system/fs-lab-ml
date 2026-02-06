import json
import os

from collections import Counter
from typing import Any, Dict, Union
from src.api_response import api_success, api_error
from src.config import RAW_DATA_DIR, RAW_DATA_FILE


def _describe(value: Any) -> Dict[str, Any]:
    return {
        "type": type(value).__name__,
        "is_null": value is None,
        "is_empty": value == {} or value == [] or value == "",
    }


# recursive analysis function
def _inspect_value(value: Any, depth: int = 0, max_depth: int = 3) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "type": type(value).__name__,
        "is_null": value is None,
    }

    # protection against endless loop
    if depth >= max_depth:
        info["truncated"] = True
        return info

    if isinstance(value, dict):
        info["keys"] = {
            k: _inspect_value(v, depth + 1, max_depth) for k, v in value.items()
        }

    elif isinstance(value, list):
        info["length"] = len(value)
        if value:
            types = Counter(type(v).__name__ for v in value)
            info["item_types"] = dict(types)

    return info


def inspect_raw_data():
    path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)

    # error warning
    if not os.path.exists(path):
        return api_error(
            code="RAW_DATA_NOT_FOUND",
            message=f"File not found: {path}",
        )

    # read-only data access
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    summary: Dict[str, Any] = {
        "root_type": type(data).__name__,
    }

    # object (dict)
    if isinstance(data, dict):
        summary["keys"] = {key: _describe(value) for key, value in data.items()}

    # list
    elif isinstance(data, list):
        summary["length"] = len(data)
        if data:
            summary["first_item_type"] = type(data[0]).__name__

    return api_success(summary)


def inspect_raw_data_deep():
    path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)

    # error warning
    if not os.path.exists(path):
        return api_error(
            code="RAW_DATA_NOT_FOUND",
            message=f"File not found: {path}",
        )

    # read-only data access
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    analysis = _inspect_value(data)

    return api_success(analysis)
