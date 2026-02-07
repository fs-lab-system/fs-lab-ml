from typing import Any, Dict

from src.api_response import api_success, api_error


def decide_service_health(features: Dict[str, Dict[str, Any]]):
    # protection if pipline is broken
    if not isinstance(features, dict):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected feature dict",
        )

    # final decisions of script
    decisions: Dict[str, Dict[str, Any]] = {}

    for service, f in features.items():
        if f["latency_class"] == "critical":
            status = "CRITICAL"
        elif not f["is_reliable"]:
            status = "UNRELIABLE"
        else:
            status = "OK"

        decisions[service] = {
            "status": status,
            "latency_class": f["latency_class"],
            "is_reliable": f["is_reliable"],
            "latency_ratio": f["latency_ratio"],
        }

    return api_success(
        {
            "by_service": decisions,
        }
    )
