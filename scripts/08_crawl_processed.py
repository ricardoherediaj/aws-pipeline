"""Create and run crawler for processed Parquet data.

Usage:
    uv run python scripts/08_crawl_processed.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.glue_client import (
    create_crawler,
    crawler_exists,
    start_crawler,
    get_crawler_status
)


def main() -> None:
    """Setup crawler for processed zone."""
    database_name = config.GLUE_DATABASE_NAME
    crawler_name = 'datalake_crawler_processed'
    bucket = config.S3_BUCKET_NAME
    s3_path = f's3://{bucket}/processed/finanzas/'

    # IAM role ARN (reusing the same role)
    account_id = "471112841755"
    role_name = "AWSGlueServiceRole-DataLake"
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"

    print(f"🕷️  Setting up Glue Crawler for Parquet data\n")

    # Create crawler if doesn't exist
    if not crawler_exists(crawler_name):
        print(f"Creating crawler for: {s3_path}")
        if not create_crawler(
            crawler_name=crawler_name,
            database_name=database_name,
            s3_path=s3_path,
            role_arn=role_arn,
            table_prefix='parquet_'
        ):
            print("❌ Failed to create crawler")
            sys.exit(1)
    else:
        print(f"✅ Crawler '{crawler_name}' already exists")

    # Start crawler
    print(f"\n▶️  Starting crawler...")
    if not start_crawler(crawler_name):
        print("❌ Failed to start crawler")
        sys.exit(1)

    # Monitor progress
    print(f"\n⏳ Monitoring crawler progress...\n")

    max_wait = 180
    elapsed = 0

    while elapsed < max_wait:
        status = get_crawler_status(crawler_name)

        if status == 'READY':
            print(f"\n✅ Crawler completed!")
            break
        elif status in ['RUNNING', 'STOPPING']:
            print(f"   [{elapsed:03d}s] Status: {status}...")
            time.sleep(10)
            elapsed += 10
        else:
            print(f"\n⚠️  Status: {status}")
            break

    print(f"\n📊 Check new Parquet tables:")
    print(f"   SHOW TABLES IN {database_name};")


if __name__ == '__main__':
    main()
