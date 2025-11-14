"""
UK Exchange scheduled jobs (LSE).
Market open: 11:00 IST
Market close: 20:30 IST
"""
import logging
from finhub_etl.loaders.in_universe import get_symbols_by_exchange, get_symbols_list
from finhub_etl.producer.connection import get_producer
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT

logger = logging.getLogger(__name__)


async def uk_market_open_job():
    """
    Job triggered at market open (11:00 IST).
    Fetches data for LSE at the start of trading.
    """
    lse_symbols = get_symbols_by_exchange("LSE")
    chix_symbols = get_symbols_by_exchange("CHIX")

    producer = get_producer()
    symbols = lse_symbols + chix_symbols

    logger.info(f"Publishing ETL tasks for {len(symbols)} symbols")

    for symbol in symbols:
        for handler_key in HANDLER_MODEL_DICT.keys():

            message = {
                "symbol": symbol,
                "handler": handler_key,
            }

            producer.publish(message, routing_key="finhub.task")

    logger.info("All granular ETL tasks published")


async def uk_market_close_job():
    """
    Job triggered at market close (20:30 IST).
    Fetches end-of-day data for LSE after trading ends.
    """
    lse_symbols = get_symbols_by_exchange("LSE")
    chix_symbols = get_symbols_by_exchange("CHIX")

    # TODO: Implement data fetching logic for market close
    pass
