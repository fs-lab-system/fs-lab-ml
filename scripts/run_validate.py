from src.data_validation.validate import validate_raw_data
import json

if __name__ == "__main__":
    result = validate_raw_data()
    print(json.dumps(result, indent=2))
