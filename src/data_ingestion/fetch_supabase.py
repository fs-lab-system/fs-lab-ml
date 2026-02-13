from src.data_ingestion.supabase_client import get_supabase_client
from src.api_response import api_success, api_error
from datetime import datetime, timedelta, timezone


# default fetch last 24 hours
def fetch_benchmark_runs(hours: int = 24):
    client = get_supabase_client()

    # calculate the span now and 24h ago
    since = datetime.now(timezone.utc) - timedelta(hours=hours)

    # select query, gte = greater than or equal
    response = (
        client.table("benchmark_runs")
        .select("*")
        .gte("created_at", since.isoformat())
        .execute()
    )

    if not response.data:
        return api_error(
            code="NO_DATA",
            message="No benchmark runs found in given time window",
        )

    return api_success(
        {
            "rows": response.data,
            "count": len(response.data),
        }
    )
