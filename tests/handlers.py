import asyncio
from pathlib import Path
import sys
from datetime import datetime, timedelta

from finhub_etl.config.handlers import (
    get_stock_symbols,
    get_company_profile,
    get_company_profile2,
    get_company_peers,
    get_company_ownership,
    get_company_news,
    get_press_release,
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
    get_historical_mcap,
)


# Handler Test Mapping Array
HANDLER_TESTS = [
    {
        "handler": get_stock_symbols,
        "name": "Stock Symbols",
        "params": {"exchange": "US"},
    },
    {
        "handler": get_company_profile,
        "name": "Company Profile (v1)",
        "params": {"symbol": "AAPL"},
    },
    {
        "handler": get_company_profile2,
        "name": "Company Profile (v2)",
        "params": {"symbol": "AAPL"},
    },
    {
        "handler": get_company_peers,
        "name": "Company Peers",
        "params": {"symbol": "AAPL"},
    },
    {
        "handler": get_company_ownership,
        "name": "Company Ownership",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_company_news,
        "name": "Company News",
        "params": {
            "symbol": "AAPL",
            "from_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "to_date": datetime.now().strftime("%Y-%m-%d"),
        },
    },
    {
        "handler": get_press_release,
        "name": "Press Releases",
        "params": {
            "symbol": "AAPL",
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_fund_ownership,
        "name": "Fund Ownership",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_institutional_profile,
        "name": "Institutional Profile",
        "params": {},
    },
    {
        "handler": get_institutional_portfolio,
        "name": "Institutional Portfolio",
        "params": {
            "cik": "0001067983",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_institutional_ownership,
        "name": "Institutional Ownership",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_company_basic_financials,
        "name": "Company Basic Financials",
        "params": {"symbol": "AAPL", "metric": "all"},
    },
    {
        "handler": get_company_financials,
        "name": "Company Financials",
        "params": {"symbol": "AAPL", "statement": "income", "freq": "annual"},
    },
    {
        "handler": get_company_reported_financials,
        "name": "Company Reported Financials",
        "params": {"symbol": "AAPL"},
    },
    {
        "handler": get_company_dividends,
        "name": "Company Dividends",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    {
        "handler": get_company_price_metrics,
        "name": "Company Price Metrics",
        "params": {"symbol": "AAPL"},
    },
    {
        "handler": get_sector_metrics,
        "name": "Sector Metrics",
        "params": {"region": "US"},
    },
    {
        "handler": get_ipo_calendar,
        "name": "IPO Calendar",
        "params": {
            "from_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            "to_date": datetime.now().strftime("%Y-%m-%d"),
        },
    },
    {
        "handler": get_historical_mcap,
        "name": "Historical Market Cap",
        "params": {
            "symbol": "AAPL",
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
        },
    },
]


async def test_handler(handler, name, params):
    """Test if handler is callable and returns data."""
    try:
        data = await handler(**params)

        if data:
            count = len(data) if isinstance(data, list) else "N/A"
            return {"status": "PASS", "count": count}
        else:
            return {"status": "FAIL", "error": "No data returned"}

    except Exception as e:
        return {"status": "FAIL", "error": str(e)}


async def run_tests():
    """Run all handler tests."""
    print("=" * 60)
    print("RUNNING HANDLER TESTS")
    print("=" * 60)
    print()

    results = []

    for idx, test in enumerate(HANDLER_TESTS, 1):
        print(f"[{idx}/{len(HANDLER_TESTS)}] Testing {test['name']}...", end=" ")

        result = await test_handler(test["handler"], test["name"], test["params"])
        result["name"] = test["name"]
        results.append(result)

        if result["status"] == "PASS":
            count_info = f" ({result['count']} records)" if result['count'] != "N/A" else ""
            print(f"[PASS]{count_info}")
        else:
            print(f"[FAIL]")
            print(f"  Error: {result['error']}")

    # Summary
    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")

    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
    print()

    if failed > 0:
        print("Failed Tests:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  - {r['name']}: {r['error']}")

    return results


async def main():
    """Main entry point."""
    print("Starting Finnhub API Handler Tests\n")
    await run_tests()
    print("\nNote: To save data to database, run: make test-store-db")


if __name__ == "__main__":
    asyncio.run(main())
