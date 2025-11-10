import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))



from src.utils.save import save_to_db
from src.models import StockSymbol
from src.config.handlers import get_stock_symbols


async def main():
    """
    Main entry point for the test script.
    """
    print("Starting database save test...")

    # Fetch stock symbols from US exchange
    print("Fetching stock symbols...")
    symbols = await get_stock_symbols(exchange="US")
    print(f"Fetched {len(symbols)} symbols")

    # Save to database
    print("Saving to database...")
    saved_symbols = await save_to_db(StockSymbol, symbols)
    print(f"\nTest completed successfully! Saved {len(saved_symbols)} symbols.")


if __name__ == "__main__":
    asyncio.run(main())