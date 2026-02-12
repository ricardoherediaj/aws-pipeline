"""Generate fake e-commerce data locally.

Usage:
    uv run python scripts/02_generate_data.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import config
from src.data_generator import generate_all_data


def main() -> None:
    """Generate data and save to local raw directory."""
    output_dir = config.RAW_DATA_DIR / 'ecommerce'
    generate_all_data(output_dir)
    print(f"\n✅ Data generated in {output_dir}")


if __name__ == '__main__':
    main()
