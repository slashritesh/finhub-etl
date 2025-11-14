"""
Example: Load matched stocks from CSV into database

This script demonstrates how to use the load_matched_stocks_csv helper function
to import stock data from a CSV file into the matched_stocks table.

Usage:
    poetry run python examples/load_matched_stocks.py
"""

import asyncio
import sys
from pathlib import Path

from finhub_etl.utils.csv_loader import load_matched_stocks_csv





async def main():
    """Load matched stocks from CSV file."""

    # Path to CSV file
    csv_path = "data/matched_stocks.csv"

    print(f"Loading matched stocks from: {csv_path}")
    print(f"File exists: {csv_path.exists()}")
    print("-" * 80)

    # Optional: Clear existing data first
    # print("Clearing existing data...")
    # cleared = await clear_matched_stocks_table()
    # print(f"Cleared {cleared} existing records\n")

    # Load CSV data into database
    try:
        total = await load_matched_stocks_csv(
            csv_path=csv_path,
            batch_size=1000,  # Insert 1000 records at a time
        )
        print("-" * 80)
        print(f"✓ Successfully loaded {total} matched stocks into database")
    except FileNotFoundError:
        print(f"✗ Error: CSV file not found at {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import warnings
    # Suppress aiomysql event loop warnings
    warnings.filterwarnings("ignore", message=".*Event loop is closed.*")
    asyncio.run(main())
