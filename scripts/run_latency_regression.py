import json

from src.data_ingestion.fetch_supabase import fetch_benchmark_runs
from src.data_validation.validate_benchmark_runs import validate_benchmark_runs
from src.data_processing.normalize_benchmark_runs import normalize_benchmark_runs
from src.data_processing.aggregate_benchmark_runs import aggregate_by_service
from src.data_processing.features_benchmark_runs import build_service_features
from src.ml.latency_regression import train_latency_regression


if __name__ == "__main__":
    rows = fetch_benchmark_runs(limit=500)["data"]["rows"]
    validate_benchmark_runs(rows)

    normalized = normalize_benchmark_runs(rows)["data"]["rows"]
    aggregates = aggregate_by_service(normalized)["data"]["by_service"]
    features = build_service_features(aggregates)["data"]["by_service"]

    result = train_latency_regression(features)
    print(json.dumps(result, indent=2))
