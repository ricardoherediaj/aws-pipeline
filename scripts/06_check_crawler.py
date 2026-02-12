"""Check Glue crawler status.

Usage:
    uv run python scripts/06_check_crawler.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.glue_client import get_crawler_status


def main() -> None:
    """Monitor crawler status until complete."""
    crawler_name = config.GLUE_CRAWLER_NAME

    print(f"⏳ Monitoring crawler: {crawler_name}\n")

    max_wait = 300  # 5 minutes
    elapsed = 0

    while elapsed < max_wait:
        status = get_crawler_status(crawler_name)

        if status == 'READY':
            print(f"\n✅ Crawler completed!")
            print(f"\n📊 Check tables created:")
            print(f"   aws glue get-tables --database-name {config.GLUE_DATABASE_NAME}")
            break
        elif status in ['RUNNING', 'STOPPING']:
            print(f"   [{elapsed:03d}s] Status: {status}...")
            time.sleep(10)
            elapsed += 10
        else:
            print(f"\n⚠️  Status: {status}")
            break

    if elapsed >= max_wait:
        print(f"\n⏱️  Timeout after {max_wait}s. Check manually:")
        print(f"   https://console.aws.amazon.com/glue/")


if __name__ == '__main__':
    main()
