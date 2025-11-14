"""
UAE Exchange scheduled jobs (ADSM, DFM).
Market open: 10:00 IST
Market close: 14:45 IST
"""

from finhub_etl.loaders.in_universe import get_symbols_by_exchange


async def uae_market_open_job():
    """
    Job triggered at market open (10:00 IST).
    Fetches data for ADSM and DFM at the start of trading.
    """
    adsm_symbols = get_symbols_by_exchange("ADSM")
    dfm_symbols = get_symbols_by_exchange("DFM")

    # TODO: Implement data fetching logic for market open
    pass


async def uae_market_close_job():
    """
    Job triggered at market close (14:45 IST).
    Fetches end-of-day data for ADSM and DFM after trading ends.
    """
    adsm_symbols = get_symbols_by_exchange("ADSM")
    dfm_symbols = get_symbols_by_exchange("DFM")

    # TODO: Implement data fetching logic for market close
    pass
