from datetime import datetime, timezone
from typing import Dict, Any

from src.data_ingestion.supabase_client import get_supabase_client


def write_service_features(features: Dict[str, Dict[str, Any]]):
    # create connection with database
    client = get_supabase_client()

    rows = []

    # get datetime in iso-format
    run_timestamp = datetime.now(timezone.utc).isoformat()

    # for each service, create a row and insert it into SQL table
    for service, feature_dict in features.items():
        # float: JSON expects serialized Values (no decimal surprises!)
        rows.append(
            {
                "run_timestamp": run_timestamp,
                "service": service,
                "p50_latency_s": float(feature_dict["p50_latency_s"]),
                "p95_latency_s": float(feature_dict["p95_latency_s"]),
                "p99_latency_s": float(feature_dict["p99_latency_s"]),
                "tail_ratio_p95_p50": float(feature_dict["tail_ratio_p95_p50"]),
                "tail_ratio_p99_p95": float(feature_dict["tail_ratio_p99_p95"]),
                "success_rate": float(feature_dict["success_rate"]),
            }
        )

    # HTTP POST: JSON body carries 3 potential new rows (go, python, node)
    # only a sigle network call !
    result = client.table("service_feature_snapshots").insert(rows).execute()

    return result
