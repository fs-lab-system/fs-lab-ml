# Data ingestion entry point
import json
import os
import requests

from src.config import DATA_SOURCE_URL, RAW_DATA_DIR, RAW_DATA_FILE
from src.api_response import api_success, api_error


def fetch_data():
    try:
        # timeout -> no blocking
        response = requests.get(DATA_SOURCE_URL, timeout=100)
        # error visible
        response.raise_for_status()

        # creates a floder, if it dosn´t exist
        os.makedirs(RAW_DATA_DIR, exist_ok=True)

        path = os.path.join(RAW_DATA_DIR, RAW_DATA_FILE)
        path = path.replace("\\", "/")
        data = response.json()

        # data persistence in file  
        with open(path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2)

        return api_success(
                data={
                    "path": path,
                    "records": len(data) if isinstance(data, list) else 1,
                }
            )
    
    except requests.RequestException as exc:
        return api_error(
            code="FETCH_FAILED",
            message=str(exc),
        )
