from src.data_ingestion.fetch_supabase import fetch_benchmark_runs
from src.data_validation.validate_benchmark_runs import validate_benchmark_runs
from src.data_processing.normalize_benchmark_runs import normalize_benchmark_runs
from src.data_processing.aggregate_benchmark_runs import aggregate_by_service
import json

if __name__ == "__main__":
    # ingestion phase
    fetch_result = fetch_benchmark_runs(limit=50)
    if not fetch_result["success"]:
        print(json.dumps(fetch_result, indent=2))
        exit(1)

    # access only the rows in data
    rows = fetch_result["data"]["rows"]

    # validation phase
    validation = validate_benchmark_runs(rows)
    if not validation["success"]:
        print(json.dumps(validation, indent=2))
        exit(1)

    # normalization phase
    normalized = normalize_benchmark_runs(rows)
    if not normalized["success"]:
        print(json.dumps(normalized, indent=2))
        exit(1)

    # aggregation phase
    aggregates = aggregate_by_service(normalized["data"]["rows"])
    print(json.dumps(aggregates, indent=2))
