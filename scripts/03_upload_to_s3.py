"""Upload finance data to S3 raw zone.

Usage:
    uv run python scripts/03_upload_to_s3.py
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.s3_client import upload_file


def main() -> None:
    """Upload finance CSV files to S3 raw zone with date partitioning."""
    bucket = config.S3_BUCKET_NAME
    local_dir = config.RAW_DATA_DIR

    # Current date for partitioning
    today = datetime.now().strftime('%Y-%m-%d')

    print(f"📤 Uploading finance data to s3://{bucket}/raw/finanzas/\n")

    # Upload all finance CSV files
    csv_files = list(local_dir.glob('finanzas_*.csv'))

    if not csv_files:
        print("❌ No finance CSV files found in data/raw/")
        print(f"   Expected files like: finanzas_customers.csv, finanzas_accounts.csv, etc.")
        sys.exit(1)

    for file_path in csv_files:
        # Extract entity name (e.g., 'customers' from 'finanzas_customers.csv')
        entity = file_path.stem.replace('finanzas_', '')

        # Create S3 key with date partitioning
        s3_key = f'raw/finanzas/{entity}/date={today}/{file_path.name}'

        upload_file(bucket, file_path, s3_key)

    print(f"\n✅ Uploaded {len(csv_files)} files to S3!")
    print(f"📊 Total entities: {', '.join(sorted([f.stem.replace('finanzas_', '') for f in csv_files]))}")


if __name__ == '__main__':
    main()
