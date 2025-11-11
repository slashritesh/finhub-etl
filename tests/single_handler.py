# -*- coding: utf-8 -*-
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
LOG_FILE = LOG_DIR / f"single_handler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

from src.database import engine
from src.database.core import get_session
from src.utils.mappings import HANDLER_MODEL_DICT as HANDLER_MODEL_TESTS


# CONFIGURATION - Change this to test different handler
TEST_HANDLER_KEY = "company_news"


async def test_handler():
    """Test single handler - fetch API and store in DB."""

    config = HANDLER_MODEL_TESTS[TEST_HANDLER_KEY]

    logger.info(f"Testing: {config['name']}")

    try:
        # Fetch from API
        data = await config["handler"](**config["params"])

        if not data:
            logger.warning("No data returned from API")
            return

        # Convert to list if single dict
        records = data if isinstance(data, list) else [data]

        # Limit if needed
        if config.get("limit"):
            records = records[:config["limit"]]

        logger.info(f"Fetched {len(records)} records")

        # Store in DB
        stored = 0
        existing = 0

        print(records)

        async for session in get_session():
            for record in records:
                try:
                    model_instance = config["model"].model_validate(record)
                    print(model_instance)
                    session.add(model_instance)
                    await session.commit()
                    stored += 1
                except IntegrityError:
                    await session.rollback()
                    existing += 1
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Error storing record: {str(e)}")

        logger.info(f"Stored: {stored}, Existing: {existing}")
        logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise


async def main():
    try:
        logger.info(f"Starting test for: {TEST_HANDLER_KEY}")
        await test_handler()
    finally:
        await engine.dispose()
        logger.info("Database engine disposed properly.")


if __name__ == "__main__":
    
    asyncio.run(main())
