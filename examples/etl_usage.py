"""
Example usage of ETL utilities for fetching and storing Finnhub data.

Run this file to see different ways to use the ETL utilities.
"""

import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def example_1_single_fetch():
    """Example 1: Fetch and store a single data point."""
    print("\n" + "="*60)
    print("Example 1: Fetch and store company profile")
    print("="*60)

    from src.config import get_company_profile
    from src.models.company import CompanyProfile
    from src.utils import fetch_and_store

    result = await fetch_and_store(
        handler_func=get_company_profile,
        model_class=CompanyProfile,
        handler_params={'symbol': 'AAPL'}
    )

    if result:
        print(f"✓ Saved company profile for {result.ticker}")
        print(f"  Name: {result.name}")
        print(f"  Market Cap: {result.marketCapitalization}")


async def example_2_with_transform():
    """Example 2: Fetch with data transformation."""
    print("\n" + "="*60)
    print("Example 2: Fetch and store company peers")
    print("="*60)

    from src.config import get_peers
    from src.models.company_data import CompanyPeer
    from src.utils import fetch_and_store, transform_peers_response

    symbol = 'AAPL'
    result = await fetch_and_store(
        handler_func=get_peers,
        model_class=CompanyPeer,
        handler_params={'symbol': symbol},
        transform_func=lambda data: transform_peers_response(data, symbol)
    )

    if result:
        print(f"✓ Saved {len(result)} peer relationships for {symbol}")
        for peer in result[:5]:
            print(f"  {peer.symbol} <-> {peer.peer}")


async def example_3_batch_operation():
    """Example 3: Batch fetch and store using mappings."""
    print("\n" + "="*60)
    print("Example 3: Batch fetch company data")
    print("="*60)

    from src.utils import batch_fetch_and_store, get_company_data_mappings

    symbol = 'MSFT'
    mappings = get_company_data_mappings(symbol)

    results = await batch_fetch_and_store(mappings)

    print(f"\n✓ Processed {len(results)} operations:")
    for name, result in results.items():
        status = "✓" if result['success'] else "✗"
        print(f"  {status} {name}: {result['count']} records")


async def example_4_market_data():
    """Example 4: Fetch market data (candles)."""
    print("\n" + "="*60)
    print("Example 4: Fetch stock candles")
    print("="*60)

    from src.utils import batch_fetch_and_store, get_market_data_mappings

    symbol = 'GOOGL'
    mappings = get_market_data_mappings(
        symbol=symbol,
        resolution='D',
        days_back=7  # Last 7 days
    )

    results = await batch_fetch_and_store(mappings)

    for name, result in results.items():
        if result['success']:
            print(f"✓ {name}: Saved {result['count']} candles")


async def example_5_news_data():
    """Example 5: Fetch news data."""
    print("\n" + "="*60)
    print("Example 5: Fetch company news")
    print("="*60)

    from src.utils import batch_fetch_and_store, get_news_mappings

    symbol = 'TSLA'
    mappings = get_news_mappings(symbol=symbol, days_back=7)

    results = await batch_fetch_and_store(mappings)

    for name, result in results.items():
        if result['success']:
            print(f"✓ {name}: Saved {result['count']} news articles")


async def example_6_full_company_data():
    """Example 6: Fetch all available data for a company."""
    print("\n" + "="*60)
    print("Example 6: Fetch complete company dataset")
    print("="*60)

    from src.utils import batch_fetch_and_store, get_full_company_mappings

    symbol = 'AAPL'
    print(f"Fetching all available data for {symbol}...")
    print("This may take a while...\n")

    mappings = get_full_company_mappings(symbol)
    results = await batch_fetch_and_store(mappings)

    print(f"\n✓ Completed {len(results)} operations:")
    success_count = sum(1 for r in results.values() if r['success'])
    total_records = sum(r['count'] for r in results.values())

    print(f"  Success: {success_count}/{len(results)}")
    print(f"  Total records: {total_records}")

    print("\nDetails:")
    for name, result in results.items():
        status = "✓" if result['success'] else "✗"
        print(f"  {status} {name}: {result['count']} records")


async def example_7_multiple_symbols():
    """Example 7: Fetch data for multiple symbols."""
    print("\n" + "="*60)
    print("Example 7: Fetch data for multiple companies")
    print("="*60)

    from src.utils import batch_fetch_and_store, get_company_data_mappings

    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

    all_mappings = []
    for symbol in symbols:
        all_mappings.extend(get_company_data_mappings(symbol))

    print(f"Fetching data for {len(symbols)} companies...")
    results = await batch_fetch_and_store(all_mappings)

    print(f"\n✓ Processed {len(results)} operations")
    print(f"  Total records: {sum(r['count'] for r in results.values())}")


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Finnhub ETL Utility Examples")
    print("="*60)

    # Run examples
    await example_1_single_fetch()
    await example_2_with_transform()
    await example_3_batch_operation()
    await example_4_market_data()
    await example_5_news_data()
    # await example_6_full_company_data()  # Uncomment for full dataset
    await example_7_multiple_symbols()

    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
