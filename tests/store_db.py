import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from src.utils.save import save_to_db
# from src.models import StockSymbol
from src.config.handlers import (
    get_stock_symbols,
    get_company_profile,
    get_company_profile2,
    get_company_news,
    get_company_peers,
    get_press_release,
    get_company_ownership,
    get_fund_ownership,
    get_institutional_profile,
    get_institutional_portfolio,
    get_institutional_ownership,
    get_company_basic_financials,
    get_company_financials,
    get_company_reported_financials,
    get_company_dividends,
    get_company_price_metrics,
    get_sector_metrics,
    get_ipo_calendar,
    get_historical_mcap
)


async def main():
    """
    Main entry point for the test script.
    """
    try:
        print("Starting database save test...")

        # Fetch stock symbols from US exchange
        print("Fetching stock symbols...")
        result = await get_company_profile(symbol="APPL")
        print(result)
        # print(f"Fetched {len(symbols)} symbols")

        # Save to database
        # print("Saving to database...")
        # saved_symbols = await save_to_db(StockSymbol, symbols)
        # print(f"\nTest completed successfully! Saved {len(saved_symbols)} symbols.")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    


if __name__ == "__main__":
    import warnings
    # Suppress aiomysql event loop warnings
    warnings.filterwarnings("ignore", message=".*Event loop is closed.*")
    asyncio.run(main())
    