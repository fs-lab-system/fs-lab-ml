from src.data_ingestion.fetch_supabase import fetch_benchmark_runs
import json

if __name__ == "__main__":
    result = fetch_benchmark_runs(limit=10)
    print(json.dumps(result, indent=2))
