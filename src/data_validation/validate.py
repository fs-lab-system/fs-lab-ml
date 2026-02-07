import json
import os
from typing import Any, Dict, List

from src.api_response import api_success, api_error
from src.config import RAW_DATA_DIR, RAW_DATA_FILE


EXPECTED_SCHEMA = {
    "slideshow": {
        "type": dict,
        "required": True,
        "keys": {
            "author": {"type": str, "required": True},
            "date": {"type": str, "required": True},
            "title": {"type": str, "required": True},
            "slides": {"type": list, "required": True},
        },
    }
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


# checks if the data has the expected schema
def validate_raw_data():
    # check for the path
    path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)
    if not os.path.exists(path):
        return api_error(
            code="RAW_DATA_NOT_FOUND",
            message=f"File not found: {path}",
        )

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # remember all validation errors
    errors: List[str] = []

    # iteration through schema and check if "data fits"
    for field, rules in EXPECTED_SCHEMA.items():
        # get real value from the data and validate "main" field type
        value = data.get(field)
        _validate_field(field, value, rules, errors)

        # only if real value is a dict and has fields like schema
        if value and isinstance(value, dict) and "keys" in rules:
            # check every single field
            for subfield, subrules in rules["keys"].items():
                # check the fields inside the "main" field
                _validate_field(
                    f"{field}.{subfield}",
                    value.get(subfield),
                    subrules,
                    errors,
                )

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
            "checked_fields": list(EXPECTED_SCHEMA.keys()),
        }
    )
