# Manual execution script
from src.data_ingestion.fetch import fetch_data
import json

if __name__ == "__main__":
    result = fetch_data()
    print(json.dumps(result, indent=2))
