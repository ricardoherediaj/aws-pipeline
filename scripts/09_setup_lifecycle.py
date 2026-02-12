"""Setup S3 Lifecycle policies for cost optimization.

Policies:
- Move raw data > 30 days to Glacier (90% cheaper)
- Delete temp files after 7 days
- Keep processed data in S3 Standard
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
import boto3
from botocore.exceptions import ClientError

def setup_lifecycle_policies(bucket_name: str) -> None:
    """Configure S3 lifecycle policies for cost optimization."""
    s3 = boto3.client('s3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )

    lifecycle_config = {
        'Rules': [
            {
                'ID': 'Archive-old-raw-data',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'raw/'},
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'GLACIER'
                    }
                ]
            },
            {
                'ID': 'Delete-temp-athena-results',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'athena-results/'},
                'Expiration': {'Days': 7}
            },
            {
                'ID': 'Archive-old-processed-data',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'processed/'},
                'Transitions': [
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    }
                ]
            }
        ]
    }

    try:
        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_config
        )
        print(f"✅ Lifecycle policies configured for {bucket_name}\n")
        print("📋 Policies:")
        print("   1. raw/ → Glacier after 30 days (90% cheaper)")
        print("   2. processed/ → Glacier after 90 days")
        print("   3. athena-results/ → Delete after 7 days")
        print(f"\n💰 Cost savings:")
        print(f"   S3 Standard: $0.023/GB/month")
        print(f"   S3 Glacier: $0.004/GB/month (83% cheaper)")

    except ClientError as e:
        print(f"❌ Failed to set lifecycle policies: {e}")
        sys.exit(1)


def main() -> None:
    """Setup lifecycle policies."""
    bucket = config.S3_BUCKET_NAME
    print(f"🔧 Configuring S3 Lifecycle Policies for {bucket}\n")
    setup_lifecycle_policies(bucket)


if __name__ == '__main__':
    main()
