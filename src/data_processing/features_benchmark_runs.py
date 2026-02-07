from typing import Any, Dict

from src.api_response import api_success


def build_service_features(aggregates: Dict[str, Dict[str, Any]]):
    features: Dict[str, Dict[str, Any]] = {}

    for service, a in aggregates.items():
        p50 = a["p50_latency_s"]
        p95 = a["p95_latency_s"]
        p99 = a["p99_latency_s"]

        features[service] = {
            # Strategy A – raw SRE percentiles
            "p50_latency_s": p50,
            "p95_latency_s": p95,
            "p99_latency_s": p99,
            # Strategy B – tail behavior
            "tail_ratio_p95_p50": round(p95 / p50, 3) if p50 > 0 else 0.0,
            "tail_ratio_p99_p95": round(p99 / p95, 3) if p95 > 0 else 0.0,
            "success_rate": a["success_rate"],
        }

    return api_success({"by_service": features})
