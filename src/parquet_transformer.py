"""Transform CSV data to Parquet format.

Benefits:
- 10x smaller file size (compression)
- 100x faster queries (columnar format)
- Cheaper Athena costs (less data scanned)
"""
import logging
from pathlib import Path
from datetime import datetime

import pandas as pd

from . import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def csv_to_parquet(csv_path: Path, parquet_path: Path) -> None:
    """Convert CSV file to Parquet format."""
    parquet_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, compression='snappy', index=False)

    csv_size = csv_path.stat().st_size
    parquet_size = parquet_path.stat().st_size
    compression_ratio = csv_size / parquet_size if parquet_size > 0 else 0

    logger.info(
        f"✅ {csv_path.name} → {parquet_path.name} "
        f"({csv_size:,} B → {parquet_size:,} B, {compression_ratio:.1f}x compression)"
    )


def transform_all_finance_data() -> None:
    """Transform all finance CSV files to Parquet."""
    raw_dir = config.RAW_DATA_DIR
    processed_dir = config.PROCESSED_DATA_DIR / 'finanzas'

    # Get current date for partitioning
    today = datetime.now().strftime('%Y-%m-%d')

    csv_files = list(raw_dir.glob('finanzas_*.csv'))

    if not csv_files:
        logger.error("❌ No CSV files found in raw directory")
        return

    logger.info(f"🔄 Transforming {len(csv_files)} CSV files to Parquet...\n")

    total_csv_size = 0
    total_parquet_size = 0

    for csv_file in csv_files:
        # Extract entity name (e.g., 'customers' from 'finanzas_customers.csv')
        entity = csv_file.stem.replace('finanzas_', '')

        # Create partitioned path
        parquet_dir = processed_dir / entity / f'date={today}'
        parquet_file = parquet_dir / f'{entity}.parquet'

        csv_to_parquet(csv_file, parquet_file)

        total_csv_size += csv_file.stat().st_size
        total_parquet_size += parquet_file.stat().st_size

    overall_ratio = total_csv_size / total_parquet_size if total_parquet_size > 0 else 0

    logger.info(f"\n📊 Summary:")
    logger.info(f"  Files transformed: {len(csv_files)}")
    logger.info(f"  Total CSV size: {total_csv_size:,} bytes ({total_csv_size / 1024:.1f} KB)")
    logger.info(f"  Total Parquet size: {total_parquet_size:,} bytes ({total_parquet_size / 1024:.1f} KB)")
    logger.info(f"  Overall compression: {overall_ratio:.1f}x")
    logger.info(f"  Savings: {(1 - 1/overall_ratio) * 100:.1f}%")
