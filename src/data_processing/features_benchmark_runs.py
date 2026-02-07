from typing import Any, Dict

from src.api_response import api_success, api_error


def build_service_features(aggregates: Dict[str, Dict[str, Any]]):
    if not isinstance(aggregates, dict):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected aggregates dict",
        )

    features: Dict[str, Dict[str, Any]] = {}

    for service, metrics in aggregates.items():
        avg_ms = metrics["avg_response_time_ms"]
        p95_ms = metrics["p95_response_time_ms"]
        success_rate = metrics["success_rate"]

        # conversion
        avg_s = avg_ms / 1000
        p95_s = p95_ms / 1000

        # shows instability
        latency_ratio = p95_ms / avg_ms if avg_ms > 0 else 0

        features[service] = {
            # normalized numeric features
            "avg_latency_s": round(avg_s, 2),
            "p95_latency_s": round(p95_s, 2),
            "latency_ratio": round(latency_ratio, 2),
            "success_rate": round(success_rate, 2),
            # derived boolean feature
            "is_reliable": success_rate >= 0.95,
            # categorical feature
            "latency_class": _latency_class(p95_s),
        }

    return api_success(
        {
            "by_service": features,
        }
    )


def _latency_class(p95_latency_s: float) -> str:
    if p95_latency_s < 1:
        return "fast"
    if p95_latency_s < 3:
        return "acceptable"
    if p95_latency_s < 6:
        return "slow"
    return "critical"
