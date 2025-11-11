# -*- coding: utf-8 -*-
"""Test script for model handlers - fetch and store data."""
import asyncio
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.exc import IntegrityError
from src.database.core import get_session
from src.database import engine
from src.utils.mappings import HANDLER_MODEL_DICT


# Change this key to test different handlers
TEST_KEY = "company_profile2"


class TestResult:
    """Store test results."""

    def __init__(self):
        self.stored: int = 0
        self.existing: int = 0
        self.errors: int = 0
        self.error_messages: List[str] = []

    def print_summary(self):
        """Print formatted results."""
        print(f"\n{'Results':<12} {'Count':>6}")
        print("-" * 20)
        print(f"{'Stored:':<12} {self.stored:>6}")
        print(f"{'Existing:':<12} {self.existing:>6}")
        print(f"{'Errors:':<12} {self.errors:>6}")

        if self.error_messages:
            print(f"\n{'Error Details':}")
            print("-" * 60)
            for i, msg in enumerate(self.error_messages[:5], 1):
                print(f"{i}. {msg}")
            if len(self.error_messages) > 5:
                print(f"... and {len(self.error_messages) - 5} more errors")


async def fetch_data(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch data from API using handler."""
    data = await config["handler"](**config["params"])

    if not data:
        return []

    # Convert to list if single record
    records = data if isinstance(data, list) else [data]

    # Apply limit if specified
    if config.get("limit"):
        records = records[:config["limit"]]

    return records


async def store_records(records: List[Dict[str, Any]], config: Dict[str, Any]) -> TestResult:
    """Store records in database."""
    result = TestResult()

    async for session in get_session():
        for record in records:
            try:
                model_instance = config["model"].model_validate(record)
                session.add(model_instance)
                await session.commit()
                result.stored += 1

            except IntegrityError:
                await session.rollback()
                result.existing += 1

            except Exception as e:
                await session.rollback()
                result.errors += 1
                error_msg = str(e)[:100]
                result.error_messages.append(error_msg)

    return result


async def test_handler(key: str) -> None:
    """Test a specific handler by key."""
    # Validate key
    if key not in HANDLER_MODEL_DICT:
        available_keys = ", ".join(HANDLER_MODEL_DICT.keys())
        print(f"\nError: '{key}' not found in HANDLER_MODEL_DICT")
        print(f"Available keys: {available_keys}")
        return

    config = HANDLER_MODEL_DICT[key]

    # Header
    print(f"\n{'='*60}")
    print(f"Testing Handler: {config['name']}")
    print(f"{'='*60}")

    # Fetch data
    print("\nFetching data from API...")
    records = await fetch_data(config)

    if not records:
        print("No data returned from API")
        return

    print(f"Fetched {len(records)} record(s)")

    # Store data
    print("\nStoring records in database...")
    result = await store_records(records, config)

    # Print results
    result.print_summary()
    print(f"{'='*60}\n")


async def main():
    """Main entry point."""
    try:
        await test_handler(TEST_KEY)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()
        print("Database engine disposed")


if __name__ == "__main__":
    asyncio.run(main())
