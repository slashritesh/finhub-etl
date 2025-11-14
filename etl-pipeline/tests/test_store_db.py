import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from finhub_etl.database import engine
from finhub_etl.utils.save import fetch_and_store_data
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_filename = log_dir / f"etl_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    # Array of keys to process
    KEYS = [
        # "recommendation_trends",
        # "market_holiday",
        # "revenue_estimate",
        # "eps_estimate",
        # "ebitda_estimate",
        # "ebit_estimate",
        # "company_profile",
        # "company_profile2",
        # "company_peers",
        # "company_executive",
        # "historical_employee_count",
        # "company_filing",
        # "price_metrics",
        # "historical_market_cap",
        # "earnings_calendar",
        # "basic_financials",
        # "stock_split",
        # "dividend",
        # "general_news",
        # "company_news",
        # "sector_metrics",
        # "market_status",
        # "realtime_quote",
        # "candlestick_data",
        # "reported_financials", 
        # "institutional_profile",
        # "fund_ownership",
        # "company_ownership",
        # "earnings_quality_score",
        # "stock_symbols"
    ]

    # Keys that need attention:
    # "press_release" - date null default value issue
    # "ipo_calendar" - need to update model
    # "company_financials" - 4 statements

    logger.info(f"Starting ETL process for {len(KEYS)} handlers")
    logger.info(f"Log file: {log_filename}")

    success_count = 0
    failure_count = 0
    failed_keys = []

    for KEY in KEYS:
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {KEY}")
        logger.info(f"{'='*60}")

        try:
            handler = HANDLER_MODEL_DICT[KEY]
            # logger.info(f"Handler configuration: {handler}")

            await fetch_and_store_data(
                handler=handler["handler"],
                model=handler["model"],
                **handler["params"],
            )
            logger.info(f"[SUCCESS] {KEY} processed successfully")
            success_count += 1

        except Exception as e:
            logger.error(f"[FAILURE] {KEY} - Error: {str(e)}", exc_info=True)
            failure_count += 1
            failed_keys.append(KEY)
            continue

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("ETL Process Summary")
    logger.info(f"{'='*60}")
    logger.info(f"Total handlers: {len(KEYS)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failure_count}")

    if failed_keys:
        logger.error(f"Failed handlers: {', '.join(failed_keys)}")

    logger.info(f"Log file saved: {log_filename}")




if __name__ == "__main__":
    asyncio.run(main())
