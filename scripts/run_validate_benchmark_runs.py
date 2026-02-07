from src.data_ingestion.fetch_supabase import fetch_benchmark_runs
from src.data_validation.validate_benchmark_runs import (
    validate_benchmark_runs,
)
import json

if __name__ == "__main__":
    fetch_result = fetch_benchmark_runs(limit=10)

    if not fetch_result["success"]:
        print(json.dumps(fetch_result, indent=2))
    else:
        rows = fetch_result["data"]["rows"]
        result = validate_benchmark_runs(rows)
        print(json.dumps(result, indent=2))
