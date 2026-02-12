"""Verify Data Lake structure and show statistics.

Usage:
    uv run python scripts/04_verify_s3.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.s3_client import list_objects


def format_size(bytes: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"


def main() -> None:
    """Show Data Lake statistics."""
    bucket = config.S3_BUCKET_NAME

    print(f"📊 Data Lake Statistics: s3://{bucket}/\n")

    # Count objects by zone
    zones = ['raw/finanzas', 'processed/finanzas', 'analytics/reports']

    for zone in zones:
        objects = list_objects(bucket, zone)
        # Filter out folder markers (objects ending with /)
        files = [obj for obj in objects if not obj.endswith('/')]

        print(f"\n📁 {zone}/")
        print(f"   Files: {len(files)}")

        if files:
            # Group by entity
            entities = {}
            for obj in files:
                parts = obj.split('/')
                if len(parts) >= 3:
                    entity = parts[2]
                    entities[entity] = entities.get(entity, 0) + 1

            for entity, count in sorted(entities.items()):
                print(f"   - {entity}: {count} file(s)")

    print(f"\n✅ Verification complete!")
    print(f"\n💡 Next steps:")
    print(f"   1. Configure Glue Crawler to catalog data")
    print(f"   2. Query with Athena")
    print(f"   3. Transform to Parquet for cost optimization")


if __name__ == '__main__':
    main()
