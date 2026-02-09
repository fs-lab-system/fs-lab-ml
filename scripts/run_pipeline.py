import argparse
import json

from src.data_ingestion.fetch_supabase import fetch_benchmark_runs
from src.data_validation.validate_benchmark_runs import validate_benchmark_runs
from src.data_processing.normalize_benchmark_runs import normalize_benchmark_runs
from src.data_processing.aggregate_benchmark_runs import aggregate_by_service
from src.data_processing.features_benchmark_runs import build_service_features


# ------------------------
# argument parsing
# ------------------------
parser = argparse.ArgumentParser(description="FS-Lab ML data pipeline")

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Run pipeline without writing results",
)

parser.add_argument(
    "--limit",
    type=int,
    default=21,
    help="Number of benchmark runs to fetch",
)

args = parser.parse_args()


# fetch → validate → normalize → aggregate → features → (optional ML) → persist
if __name__ == "__main__":
    # ingestion phase (limit of rows from args)
    fetch_result = fetch_benchmark_runs(limit=args.limit)
    if not fetch_result["success"]:
        print(json.dumps(fetch_result, indent=2))
        exit(1)

    # access only the rows in data
    rows = fetch_result["data"]["rows"]

    # validation phase
    if not validate_benchmark_runs(rows)["success"]:
        exit(1)

    # normalization phase
    normalized = normalize_benchmark_runs(rows)
    if not normalized["success"]:
        print(json.dumps(normalized, indent=2))
        exit(1)

    # aggregation phase
    aggregates = aggregate_by_service(normalized["data"]["rows"])

    # feature phase
    features = build_service_features(aggregates["data"]["by_service"])

    # in case of dry run , no persistence!
    if args.dry_run:
        print(json.dumps(features, indent=2))
    else:
        # later: write_features_to_supabase(features)
        print("Pipeline completed (write mode)")
