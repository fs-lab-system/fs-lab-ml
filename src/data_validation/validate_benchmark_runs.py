from typing import Any, Dict, List

from src.api_response import api_success, api_error


EXPECTED_ROW_SCHEMA: Dict[str, Dict[str, Any]] = {
    "id": {"type": str, "required": True},
    "service": {"type": str, "required": True},
    "endpoint": {"type": str, "required": True},
    "response_time_ms": {"type": int, "required": True},
    "status_code": {"type": int, "required": True},
    "region": {"type": str, "required": True},
    "created_at": {"type": str, "required": True},  # ISO timestamp
}


# validate one field against one rule
def _validate_field(
    name: str, value: Any, rules: Dict[str, Any], errors: List[str]
) -> None:
    if value is None:
        if rules.get("required"):
            errors.append(f"Missing required field: {name}")
        return

    expected_type = rules.get("type")
    if expected_type and not isinstance(value, expected_type):
        errors.append(
            f"Field '{name}' has type {type(value).__name__}, "
            f"expected {expected_type.__name__}"
        )


def validate_benchmark_runs(rows: List[Dict[str, Any]]):
    if not isinstance(rows, list):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected list of rows",
        )

    errors: List[str] = []

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"Row {index} is not an object")
            continue

        for field, rules in EXPECTED_ROW_SCHEMA.items():
            _validate_field(
                f"row[{index}].{field}",
                row.get(field),
                rules,
                errors,
            )

        # simple sanity checks (not ML, just hygiene)
        if isinstance(row.get("response_time_ms"), int):
            if row["response_time_ms"] < 0:
                errors.append(f"row[{index}].response_time_ms must be >= 0")

        if isinstance(row.get("status_code"), int):
            if not (100 <= row["status_code"] <= 599):
                errors.append(f"row[{index}].status_code out of HTTP range")

    # return error response
    if errors:
        return api_error(
            code="VALIDATION_FAILED",
            message="; ".join(errors),
        )

    # return success response
    return api_success(
        {
            "status": "valid",
            "rows_checked": len(rows),
        }
    )
