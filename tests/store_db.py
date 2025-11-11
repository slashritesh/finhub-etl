import asyncio
from pathlib import Path
import sys
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"store_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also log to console
    ]
)

logger = logging.getLogger(__name__)

from src.database.core import get_session
from src.utils.mappings import HANDLER_MODEL_TESTS


async def test_store_handler(handler, name, params, model, data_key, limit, transform=None):
    """Test if handler data can be fetched and stored in database."""
    try:
        # Step 1: Fetch data from API
        logger.info(f"Testing {name}: Fetching data from API with params {params}")
        print(f"Fetching data from API...", end=" ")
        data = await handler(**params)

        if not data:
            logger.warning(f"{name}: No data returned from API")
            return {
                "status": "SKIP",
                "reason": "No data returned from API",
                "fetched": 0,
                "stored": 0,
            }

        # Extract data based on data_key
        if data_key and isinstance(data, dict):
            records = data.get(data_key, [])
        else:
            records = data

        # Handle single dict records (e.g., CompanyProfile)
        if isinstance(records, dict):
            records = [records]

        # Transform data if needed
        if transform:
            symbol = params.get("symbol", None)
            records = transform(records, symbol)
            if isinstance(records, dict):
                records = [records]

        # Limit records for testing
        if limit:
            records = records[:limit]

        fetched_count = len(records) if isinstance(records, list) else 1
        logger.info(f"{name}: Fetched {fetched_count} records from API")
        print(f"[{fetched_count} records]", end=" ")

        # Step 2: Store in database
        print(f"Storing...", end=" ")
        stored_count = 0
        skipped_count = 0

        async for session in get_session():
            for record in records:
                try:
                    # Create model instance
                    model_instance = model.model_validate(record)
                    session.add(model_instance)
                    await session.commit()
                    stored_count += 1
                except IntegrityError:
                    # Record already exists (duplicate key)
                    await session.rollback()
                    skipped_count += 1
                except Exception as e:
                    await session.rollback()
                    error_msg = str(e)[:100]
                    logger.error(f"{name}: Error storing record: {error_msg}")
                    print(f"\n    Error storing record: {error_msg}")
                    continue

        logger.info(f"{name}: Stored {stored_count} records, skipped {skipped_count} duplicates")

        # Step 3: Verify data in database
        print(f"Verifying...", end=" ")
        async for session in get_session():
            result = await session.execute(select(model).limit(1))
            db_records = result.scalars().all()
            exists = len(db_records) > 0

        if not exists and stored_count == 0:
            logger.error(f"{name}: No records found in database after storage attempt")
            return {
                "status": "FAIL",
                "reason": "No records in database",
                "fetched": fetched_count,
                "stored": stored_count,
                "skipped": skipped_count,
            }

        logger.info(f"{name}: Test PASSED - Data verified in database")
        return {
            "status": "PASS",
            "fetched": fetched_count,
            "stored": stored_count,
            "skipped": skipped_count,
        }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"{name}: Test FAILED with exception: {error_msg}")
        return {
            "status": "FAIL",
            "reason": error_msg,
            "fetched": 0,
            "stored": 0,
            "skipped": 0,
        }


async def run_tests():
    """Run all handler to database storage tests."""
    logger.info("=" * 80)
    logger.info("STARTING DATABASE STORAGE TESTS")
    logger.info("=" * 80)

    print("=" * 80)
    print("RUNNING DATABASE STORAGE TESTS")
    print("=" * 80)
    print()

    results = []

    for idx, test in enumerate(HANDLER_MODEL_TESTS, 1):
        print(f"[{idx}/{len(HANDLER_MODEL_TESTS)}] Testing {test['name']}...")
        logger.info(f"[{idx}/{len(HANDLER_MODEL_TESTS)}] Starting test: {test['name']}")

        result = await test_store_handler(
            test["handler"],
            test["name"],
            test["params"],
            test["model"],
            test.get("data_key"),
            test.get("limit"),
            test.get("transform"),
        )
        result["name"] = test["name"]
        results.append(result)

        if result["status"] == "PASS":
            print(
                f"  [PASS] Fetched: {result['fetched']}, "
                f"Stored: {result['stored']}, "
                f"Skipped: {result['skipped']}"
            )
        elif result["status"] == "SKIP":
            print(f"  [SKIP] {result['reason']}")
        else:
            print(f"  [FAIL] {result.get('reason', 'Unknown error')}")

        print()

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    total_fetched = sum(r.get("fetched", 0) for r in results)
    total_stored = sum(r.get("stored", 0) for r in results)
    total_skipped = sum(r.get("skipped", 0) for r in results)

    summary = (
        f"Tests: {len(results)} | Passed: {passed} | Failed: {failed} | Skipped: {skipped}\n"
        f"Records: Fetched: {total_fetched} | Stored: {total_stored} | Skipped: {total_skipped}"
    )

    print(summary)
    logger.info("=" * 80)
    logger.info("TEST SUMMARY")
    logger.info(summary)
    print()

    if failed > 0:
        print("Failed Tests:")
        logger.warning("Failed Tests:")
        for r in results:
            if r["status"] == "FAIL":
                failure_msg = f"  - {r['name']}: {r.get('reason', 'Unknown error')}"
                print(failure_msg)
                logger.warning(failure_msg)

    logger.info("=" * 80)
    logger.info("DATABASE STORAGE TESTS COMPLETED")
    logger.info("=" * 80)

    return results


async def main():
    """Main entry point."""
    print("Starting Database Storage Tests\n")
    print(f"Log file: {LOG_FILE}\n")

    logger.info("Database Storage Tests Started")
    logger.info(f"Log file: {LOG_FILE}")

    await run_tests()

    print("\nNote: This test fetches data from Finnhub API and stores it in the database")
    print(f"Detailed logs saved to: {LOG_FILE}")

    logger.info("Database Storage Tests Finished")
    logger.info(f"Logs saved to: {LOG_FILE}")


if __name__ == "__main__":
    import warnings

    # Suppress aiomysql event loop warnings
    warnings.filterwarnings("ignore", message=".*Event loop is closed.*")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Tests interrupted by user")
        print("\n\nTests interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {str(e)}")
        print(f"\nUnexpected error: {str(e)}")
        raise
