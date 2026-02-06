from src.data_inspection.inspect import inspect_raw_data
import json

if __name__ == "__main__":
    result = inspect_raw_data()
    print(json.dumps(result, indent=2))
