from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID
from dateutil.parser import isoparse

from src.api_response import api_success, api_error


# expects list of dictionary
def normalize_benchmark_runs(rows: List[Dict[str, Any]]):
    if not isinstance(rows, list):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected list of rows",
        )

    # collection of clean and normalized rows
    normalized: List[Dict[str, Any]] = []

    # iterate through all rows and normalize/cast the type correctly
    for index, row in enumerate(rows):
        try:
            normalized.append(
                {
                    "id": UUID(row["id"]),
                    "service": row["service"],
                    "endpoint": row["endpoint"],
                    "response_time_ms": int(row["response_time_ms"]),
                    "status_code": int(row["status_code"]),
                    "region": row["region"],
                    "created_at": isoparse(row["created_at"]),
                }
            )
        except Exception as exc:
            return api_error(
                code="NORMALIZATION_FAILED",
                message=f"Row {index}: {exc}",
            )

    return api_success(
        {
            "rows": normalized,
            "rows_normalized": len(normalized),
        }
    )
