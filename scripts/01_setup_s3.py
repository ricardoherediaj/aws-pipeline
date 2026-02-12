"""Setup S3 Data Lake structure.

Usage:
    uv run python scripts/01_setup_s3.py
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.s3_client import create_bucket, setup_data_lake_structure


def main() -> None:
    """Create bucket and folder structure."""
    bucket = config.S3_BUCKET_NAME
    region = config.AWS_REGION

    print(f"🚀 Setting up Data Lake: {bucket}")
    print(f"📍 Region: {region}\n")

    # Create bucket
    if not create_bucket(bucket, region):
        print("❌ Failed to create bucket")
        sys.exit(1)

    # Create folder structure
    print("\n📁 Creating folder structure...")
    setup_data_lake_structure(bucket)

    print(f"\n✅ Data Lake ready at s3://{bucket}/")
    print("\nStructure:")
    print("├── raw/ecommerce/")
    print("├── processed/ecommerce/")
    print("├── analytics/reports/")
    print("└── athena-results/")


if __name__ == '__main__':
    main()
