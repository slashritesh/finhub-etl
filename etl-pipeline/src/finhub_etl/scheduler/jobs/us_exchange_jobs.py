"""
US Exchange scheduled jobs (NYSE, NSDQ, AMEX).
Pre-market open: 12:00 IST (4:00 AM ET)
Post-market close: 04:00 IST (8:00 PM ET)
"""

from finhub_etl.loaders.in_universe import get_symbols_by_exchange


async def us_premarket_open_job():
    """
    Job triggered at pre-market open (12:00 IST).
    Fetches data for NYSE, NASDAQ, and AMEX at the start of pre-market trading.
    """
    nyse_symbols = get_symbols_by_exchange("NYSE")
    nasdaq_symbols = get_symbols_by_exchange("NSDQ")
    amex_symbols = get_symbols_by_exchange("AMEX")

    # TODO: Implement data fetching logic for pre-market open
    pass


async def us_postmarket_close_job():
    """
    Job triggered at post-market close (04:00 IST).
    Fetches end-of-day data for NYSE, NASDAQ, and AMEX after post-market trading ends.
    """
    nyse_symbols = get_symbols_by_exchange("NYSE")
    nasdaq_symbols = get_symbols_by_exchange("NSDQ")
    amex_symbols = get_symbols_by_exchange("AMEX")

    # TODO: Implement data fetching logic for post-market close
    pass
