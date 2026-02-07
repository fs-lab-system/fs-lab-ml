from src.data_ingestion.supabase_client import get_supabase_client
from src.api_response import api_success, api_error


def fetch_benchmark_runs(limit: int = 100):
    try:
        client = get_supabase_client()

        response = (
            client.table("benchmark_runs")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

        return api_success(
            {
                "rows": response.data,
                "count": len(response.data),
            }
        )

    except Exception as exc:
        return api_error(
            code="SUPABASE_FETCH_FAILED",
            message=str(exc),
        )
