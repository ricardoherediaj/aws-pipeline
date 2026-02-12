"""Transform CSV data to Parquet and upload to S3.

Usage:
    uv run python scripts/07_transform_to_parquet.py
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.parquet_transformer import transform_all_finance_data
from src.s3_client import upload_file


def main() -> None:
    """Transform CSV to Parquet and upload to S3 processed zone."""
    bucket = config.S3_BUCKET_NAME
    processed_dir = config.PROCESSED_DATA_DIR / 'finanzas'

    print("🔄 Step 1: Transforming CSV to Parquet locally...\n")
    transform_all_finance_data()

    print("\n📤 Step 2: Uploading Parquet files to S3...\n")

    # Get current date for partitioning
    today = datetime.now().strftime('%Y-%m-%d')

    # Find all parquet files
    parquet_files = list(processed_dir.rglob('*.parquet'))

    if not parquet_files:
        print("❌ No Parquet files found")
        sys.exit(1)

    uploaded = 0
    for parquet_file in parquet_files:
        # Extract entity name from path
        entity = parquet_file.parent.parent.name

        # Create S3 key
        s3_key = f'processed/finanzas/{entity}/date={today}/{parquet_file.name}'

        if upload_file(bucket, parquet_file, s3_key):
            uploaded += 1

    print(f"\n✅ Transformation complete!")
    print(f"   Files uploaded: {uploaded}/{len(parquet_files)}")
    print(f"\n📊 Next steps:")
    print(f"   1. Run Glue Crawler on processed zone")
    print(f"   2. Query Parquet tables with Athena (100x faster)")


if __name__ == '__main__':
    main()
