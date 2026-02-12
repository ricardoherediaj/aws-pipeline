"""Configuration management for Data Lake pipeline."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# S3 Configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "rherediaiam-datalake")
S3_RAW_PREFIX = os.getenv("S3_RAW_PREFIX", "raw/")
S3_PROCESSED_PREFIX = os.getenv("S3_PROCESSED_PREFIX", "processed/")
S3_ANALYTICS_PREFIX = os.getenv("S3_ANALYTICS_PREFIX", "analytics/")

# Glue Configuration
GLUE_DATABASE_NAME = os.getenv("GLUE_DATABASE_NAME", "datalake_db")
GLUE_CRAWLER_NAME = os.getenv("GLUE_CRAWLER_NAME", "datalake_crawler")

# Athena Configuration
ATHENA_OUTPUT_LOCATION = os.getenv(
    "ATHENA_OUTPUT_LOCATION",
    f"s3://{S3_BUCKET_NAME}/athena-results/"
)

# Local paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ANALYTICS_DATA_DIR = DATA_DIR / "analytics"

# Ensure local directories exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ANALYTICS_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
