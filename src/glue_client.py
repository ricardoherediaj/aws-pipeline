"""AWS Glue client for Data Catalog operations.

Principles applied:
- Functions < 20 lines
- Single responsibility
- Type hints mandatory
- Logging over print
"""
import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _get_glue_client():
    """Create configured Glue client."""
    return boto3.client(
        'glue',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )


def _get_iam_client():
    """Create configured IAM client."""
    return boto3.client(
        'iam',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )


def database_exists(database_name: str) -> bool:
    """Check if Glue database exists."""
    glue = _get_glue_client()
    try:
        glue.get_database(Name=database_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            return False
        raise


def create_database(database_name: str, description: str = '') -> bool:
    """Create Glue database if it doesn't exist."""
    if database_exists(database_name):
        logger.info(f"✅ Database '{database_name}' already exists")
        return True

    glue = _get_glue_client()
    try:
        glue.create_database(
            DatabaseInput={
                'Name': database_name,
                'Description': description or f'Data Lake database for {database_name}'
            }
        )
        logger.info(f"✅ Created database '{database_name}'")
        return True
    except ClientError as e:
        logger.error(f"❌ Failed to create database: {e}")
        return False


def create_crawler_role(role_name: str = 'AWSGlueServiceRole-DataLake') -> str:
    """Create IAM role for Glue crawler."""
    import json

    iam = _get_iam_client()

    # Trust policy for Glue service
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "glue.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        # Try to get existing role
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        logger.info(f"✅ Using existing role '{role_name}'")
        return role_arn
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchEntity':
            raise

    # Create new role
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for AWS Glue crawler to access S3'
        )

        # Attach managed policies
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
        )
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
        )

        role_arn = response['Role']['Arn']
        logger.info(f"✅ Created role '{role_name}'")
        return role_arn
    except ClientError as e:
        logger.error(f"❌ Failed to create role: {e}")
        raise


def crawler_exists(crawler_name: str) -> bool:
    """Check if Glue crawler exists."""
    glue = _get_glue_client()
    try:
        glue.get_crawler(Name=crawler_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityNotFoundException':
            return False
        raise


def create_crawler(
    crawler_name: str,
    database_name: str,
    s3_path: str,
    role_arn: str,
    table_prefix: str = ''
) -> bool:
    """Create Glue crawler for S3 data source."""
    if crawler_exists(crawler_name):
        logger.info(f"✅ Crawler '{crawler_name}' already exists")
        return True

    glue = _get_glue_client()
    try:
        glue.create_crawler(
            Name=crawler_name,
            Role=role_arn,
            DatabaseName=database_name,
            Description=f'Crawler for {s3_path}',
            Targets={'S3Targets': [{'Path': s3_path}]},
            TablePrefix=table_prefix,
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            },
        )
        logger.info(f"✅ Created crawler '{crawler_name}'")
        return True
    except ClientError as e:
        logger.error(f"❌ Failed to create crawler: {e}")
        return False


def start_crawler(crawler_name: str) -> bool:
    """Start Glue crawler."""
    glue = _get_glue_client()
    try:
        glue.start_crawler(Name=crawler_name)
        logger.info(f"🚀 Started crawler '{crawler_name}'")
        return True
    except ClientError as e:
        if 'CrawlerRunningException' in str(e):
            logger.info(f"⏳ Crawler '{crawler_name}' is already running")
            return True
        logger.error(f"❌ Failed to start crawler: {e}")
        return False


def get_crawler_status(crawler_name: str) -> Optional[str]:
    """Get crawler status."""
    glue = _get_glue_client()
    try:
        response = glue.get_crawler(Name=crawler_name)
        state = response['Crawler']['State']
        return state
    except ClientError as e:
        logger.error(f"❌ Failed to get crawler status: {e}")
        return None
