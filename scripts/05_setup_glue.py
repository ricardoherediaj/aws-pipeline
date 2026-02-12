"""Setup AWS Glue Crawler and Data Catalog.

Usage:
    uv run python scripts/05_setup_glue.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.glue_client import (
    create_database,
    create_crawler_role,
    create_crawler,
    start_crawler,
    get_crawler_status
)


def main() -> None:
    """Setup Glue database and crawler."""
    database_name = config.GLUE_DATABASE_NAME
    crawler_name = config.GLUE_CRAWLER_NAME
    bucket = config.S3_BUCKET_NAME
    s3_path = f's3://{bucket}/raw/finanzas/'

    print(f"🔧 Setting up AWS Glue Data Catalog\n")

    # Step 1: Create database
    print("📚 Step 1: Creating Glue database...")
    if not create_database(database_name, 'Finance Data Lake database'):
        print("❌ Failed to create database")
        sys.exit(1)

    # Step 2: Create IAM role for crawler
    print("\n🔐 Step 2: Creating IAM role for crawler...")
    try:
        role_arn = create_crawler_role()
        print(f"   Role ARN: {role_arn}")
        # Wait for IAM role to propagate
        print("   ⏳ Waiting 10 seconds for IAM propagation...")
        time.sleep(10)
    except Exception as e:
        print(f"❌ Failed to create role: {e}")
        sys.exit(1)

    # Step 3: Create crawler
    print(f"\n🕷️  Step 3: Creating Glue crawler...")
    print(f"   Target: {s3_path}")
    if not create_crawler(
        crawler_name=crawler_name,
        database_name=database_name,
        s3_path=s3_path,
        role_arn=role_arn,
        table_prefix='finanzas_'
    ):
        print("❌ Failed to create crawler")
        sys.exit(1)

    # Step 4: Start crawler
    print(f"\n▶️  Step 4: Starting crawler...")
    if not start_crawler(crawler_name):
        print("❌ Failed to start crawler")
        sys.exit(1)

    # Monitor crawler status
    print(f"\n⏳ Monitoring crawler progress...")
    print(f"   (This may take 1-3 minutes)\n")

    max_wait = 180  # 3 minutes
    elapsed = 0
    while elapsed < max_wait:
        status = get_crawler_status(crawler_name)
        if status == 'READY':
            print(f"✅ Crawler completed successfully!")
            break
        elif status in ['RUNNING', 'STOPPING']:
            print(f"   Status: {status}... ({elapsed}s)")
            time.sleep(10)
            elapsed += 10
        else:
            print(f"⚠️  Unexpected status: {status}")
            break

    print(f"\n✅ Glue setup complete!")
    print(f"\n📊 Next steps:")
    print(f"   1. Check Glue Console: https://console.aws.amazon.com/glue/")
    print(f"   2. View tables in database: {database_name}")
    print(f"   3. Query data with Athena")


if __name__ == '__main__':
    main()
