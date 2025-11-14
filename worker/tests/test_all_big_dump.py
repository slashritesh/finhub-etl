import asyncio
import logging
from datetime import datetime
from pathlib import Path
# from worker.database import engine
from worker.utils.save import fetch_and_store_data
from worker.utils.mappings import HANDLER_MODEL_DICT
from worker.loaders.in_universe import get_symbols_list

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

log_filename = log_dir / f"etl_big_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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
    """
    Process all handlers for all symbols dynamically loaded from CSV.
    This is a comprehensive ETL test that processes the entire universe of stocks.
    """

    # Load symbols from CSV
    try:
        symbols = get_symbols_list()
        logger.info(f"Loaded {len(symbols)} symbols from CSV")
    except Exception as e:
        logger.error(f"Failed to load symbols: {str(e)}")
        return

    # Array of keys to process - configure which handlers to run
    KEYS = [
        "recommendation_trends",
        "market_holiday",
        "revenue_estimate",
        "eps_estimate",
        "ebitda_estimate",
        "ebit_estimate",
        "company_profile",
        "company_profile2",
        "company_peers",
        "company_executive",
        "historical_employee_count",
        "company_filing",
        "price_metrics",
        "historical_market_cap",
        "earnings_calendar",
        "basic_financials",
        "stock_split",
        "dividend",
        "general_news",
        "company_news",
        "sector_metrics",
        "market_status",
        "realtime_quote",
        "candlestick_data",
        "reported_financials",
        "institutional_profile",
        "fund_ownership",
        "company_ownership",
        "earnings_quality_score"
    ]

    logger.info(f"Starting ETL process for {len(symbols)} symbols x {len(KEYS)} handlers = {len(symbols) * len(KEYS)} total operations")
    logger.info(f"Log file: {log_filename}")

    total_success = 0
    total_failure = 0
    symbol_results = {}

    for idx, symbol in enumerate(symbols, 1):
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing Symbol {idx}/{len(symbols)}: {symbol}")
        logger.info(f"{'='*80}")

        symbol_success = 0
        symbol_failure = 0
        failed_keys = []

        for KEY in KEYS:
            logger.info(f"\n{'-'*60}")
            logger.info(f"Symbol: {symbol} | Handler: {KEY}")
            logger.info(f"{'-'*60}")

            try:
                handler_config = HANDLER_MODEL_DICT[KEY]

                # Merge symbol into params
                params = handler_config["params"].copy()
                params["symbol"] = symbol

                await fetch_and_store_data(
                    handler=handler_config["handler"],
                    model=handler_config["model"],
                    **params,
                )

                logger.info(f"[SUCCESS] {symbol} - {KEY} processed successfully")
                symbol_success += 1
                total_success += 1

            except Exception as e:
                logger.error(f"[FAILURE] {symbol} - {KEY} - Error: {str(e)}", exc_info=True)
                symbol_failure += 1
                total_failure += 1
                failed_keys.append(KEY)
                continue

        # Symbol summary
        symbol_results[symbol] = {
            "success": symbol_success,
            "failure": symbol_failure,
            "failed_keys": failed_keys
        }

        logger.info(f"\nSymbol {symbol} Summary: {symbol_success} succeeded, {symbol_failure} failed")

    # Final Summary
    logger.info(f"\n{'='*80}")
    logger.info("ETL Big Dump Summary")
    logger.info(f"{'='*80}")
    logger.info(f"Total symbols: {len(symbols)}")
    logger.info(f"Total handlers per symbol: {len(KEYS)}")
    logger.info(f"Total operations: {len(symbols) * len(KEYS)}")
    logger.info(f"Total successful: {total_success}")
    logger.info(f"Total failed: {total_failure}")
    logger.info(f"Success rate: {(total_success / (total_success + total_failure) * 100):.2f}%" if (total_success + total_failure) > 0 else "N/A")

    # Symbols with failures
    failed_symbols = {symbol: data for symbol, data in symbol_results.items() if data["failure"] > 0}
    if failed_symbols:
        logger.error(f"\n{len(failed_symbols)} symbols had failures:")
        for symbol, data in failed_symbols.items():
            logger.error(f"  {symbol}: {data['failure']} failures in {', '.join(data['failed_keys'])}")

    logger.info(f"\nLog file saved: {log_filename}")


if __name__ == "__main__":
    asyncio.run(main())



