"""S3 client for Data Lake operations.

Principles applied:
- Functions < 20 lines
- Single responsibility
- Type hints mandatory
- Logging over print
"""
import logging
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_s3_client():
    """Create configured S3 client."""
    return boto3.client(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )


def bucket_exists(bucket_name: str) -> bool:
    """Check if S3 bucket exists."""
    s3 = _get_s3_client()
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False


def create_bucket(bucket_name: str, region: str = 'us-east-1') -> bool:
    """Create S3 bucket if it doesn't exist."""
    if bucket_exists(bucket_name):
        logger.info(f"✅ Bucket '{bucket_name}' already exists")
        return True

    s3 = _get_s3_client()
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        logger.info(f"✅ Created bucket '{bucket_name}'")
        return True
    except ClientError as e:
        logger.error(f"❌ Failed to create bucket: {e}")
        return False


def create_folder(bucket_name: str, folder_path: str) -> None:
    """Create folder in S3 (empty object with trailing /)."""
    s3 = _get_s3_client()
    s3.put_object(Bucket=bucket_name, Key=folder_path, Body=b'')
    logger.info(f"📁 s3://{bucket_name}/{folder_path}")


def setup_data_lake_structure(bucket_name: str) -> None:
    """
    Create Data Lake folder structure for finance domain.

    Structure:
        raw/finanzas/{customers,accounts,transactions,...}/
        processed/finanzas/{customers,accounts,transactions,...}/
        analytics/reports/{daily_transactions,customer_metrics}/
        athena-results/
    """
    entities = ['customers', 'accounts', 'transactions', 'cards', 'loans',
                'loan_payments', 'transfers', 'investments', 'exchange_rates',
                'branches', 'bank_employees', 'account_types']

    folders = [
        *[f'raw/finanzas/{entity}/' for entity in entities],
        *[f'processed/finanzas/{entity}/' for entity in entities],
        'analytics/reports/daily_transactions/',
        'analytics/reports/customer_metrics/',
        'analytics/reports/loan_analysis/',
        'athena-results/',
    ]

    for folder in folders:
        create_folder(bucket_name, folder)


def upload_file(bucket_name: str, local_path: Path, s3_key: str) -> bool:
    """Upload file to S3."""
    s3 = _get_s3_client()
    try:
        s3.upload_file(str(local_path), bucket_name, s3_key)
        logger.info(f"✅ {local_path.name} → s3://{bucket_name}/{s3_key}")
        return True
    except ClientError as e:
        logger.error(f"❌ Upload failed: {e}")
        return False


def download_file(bucket_name: str, s3_key: str, local_path: Path) -> bool:
    """Download file from S3."""
    s3 = _get_s3_client()
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(bucket_name, s3_key, str(local_path))
        logger.info(f"✅ s3://{bucket_name}/{s3_key} → {local_path}")
        return True
    except ClientError as e:
        logger.error(f"❌ Download failed: {e}")
        return False


def list_objects(bucket_name: str, prefix: str = '') -> list[str]:
    """List object keys in S3 bucket with prefix."""
    s3 = _get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        keys = [obj['Key'] for obj in response.get('Contents', [])]
        logger.info(f"📋 Found {len(keys)} objects with prefix '{prefix}'")
        return keys
    except ClientError as e:
        logger.error(f"❌ List failed: {e}")
        return []
