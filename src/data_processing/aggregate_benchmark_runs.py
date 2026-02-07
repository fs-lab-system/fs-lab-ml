from typing import Any, Dict, List
from statistics import mean
import math

from src.api_response import api_success, api_error


def _percentile(values: List[int], p: float) -> int:
    if not values:
        return 0

    # percentiles only work in a sorted way
    values_sorted = sorted(values)

    # pick the position in the percentile (example: p50, p95 ...)
    k = math.ceil((p / 100) * len(values_sorted)) - 1
    return values_sorted[max(0, min(k, len(values_sorted) - 1))]


def aggregate_by_service(rows: List[Dict[str, Any]]):
    if not isinstance(rows, list):
        return api_error(
            code="INVALID_PAYLOAD",
            message="Expected list of rows",
        )

    # all rows of one service in one bucket
    buckets: Dict[str, List[Dict[str, Any]]] = {}

    # group by service
    for row in rows:
        service = row["service"]
        buckets.setdefault(service, []).append(row)

    aggregates: Dict[str, Dict[str, Any]] = {}

    for service, items in buckets.items():
        # extraction of data to be measured
        response_times = [r["response_time_ms"] for r in items]
        success_count = sum(1 for r in items if 200 <= r["status_code"] < 300)

        # average Baseline
        aggregates[service] = {
            "count": len(items),
            "avg_response_time_ms": int(mean(response_times)),
            "p95_response_time_ms": _percentile(response_times, 95),
            "success_rate": success_count / len(items),
        }

    return api_success(
        {
            "by_service": aggregates,
        }
    )
