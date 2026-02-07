import math
from statistics import mean
from typing import Any, Dict, List

from src.api_response import api_success, api_error


def _percentile(values: List[int], p: float) -> float:
    if not values:
        return 0.0

    values_sorted = sorted(values)
    k = math.ceil((p / 100) * len(values_sorted)) - 1
    k = max(0, min(k, len(values_sorted) - 1))
    return float(values_sorted[k])


def aggregate_by_service(rows: List[Dict[str, Any]]):
    if not isinstance(rows, list):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected list of rows",
        )

    buckets: Dict[str, List[Dict[str, Any]]] = {}

    for row in rows:
        buckets.setdefault(row["service"], []).append(row)

    aggregates: Dict[str, Dict[str, Any]] = {}

    for service, items in buckets.items():
        response_times = [r["response_time_ms"] for r in items]
        success_count = sum(1 for r in items if 200 <= r["status_code"] < 300)

        p50 = _percentile(response_times, 50)
        p95 = _percentile(response_times, 95)
        p99 = _percentile(response_times, 99)

        aggregates[service] = {
            "count": len(items),
            "p50_latency_s": round(p50 / 1000, 3),
            "p95_latency_s": round(p95 / 1000, 3),
            "p99_latency_s": round(p99 / 1000, 3),
            "success_rate": success_count / len(items),
        }

    return api_success({"by_service": aggregates})
