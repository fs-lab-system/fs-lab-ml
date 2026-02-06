# Central configuration (to be extended)
import os

# reads ENV variable
DATA_SOURCE_URL = os.getenv(
    "DATA_SOURCE_URL", "https://httpbin.org/json"  # Default only for Dev/Test
)

RAW_DATA_DIR = "data/raw"
RAW_DATA_FILE = "data.json"
