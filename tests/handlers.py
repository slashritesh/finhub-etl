import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import asyncio
from src.database.core import engine
from src.config.handlers import (
    get_company_profile,
    get_quote,
    get_company_news,
    get_earnings_calendar,
    get_basic_financials,
    get_recommendation_trends,
    get_institutional_ownership,
    get_peers,
)

# Load environment variables from .env file
load_dotenv()


async def main():
    try:
        symbol = "AAPL"
        print(f"\n{'='*60}")
        print(f"Testing Finnhub API Handlers for {symbol}")
        print(f"{'='*60}\n")

        # Test 1: Company Profile
        print(f"1. Fetching company profile for {symbol}...")
        profile = await get_company_profile(symbol)
        print(f"   Company: {profile.get('name', 'N/A')}")
        print(f"   Industry: {profile.get('finnhubIndustry', 'N/A')}")
        print(f"   Market Cap: ${profile.get('marketCapitalization', 0):,.0f}M\n")

        # Test 2: Quote Data
        print(f"2. Fetching current quote for {symbol}...")
        quote = await get_quote(symbol)
        print(f"   Current Price: ${quote.get('c', 0):.2f}")
        print(f"   Change: ${quote.get('d', 0):.2f} ({quote.get('dp', 0):.2f}%)\n")

        # Test 3: Company News
        print(f"3. Fetching recent news for {symbol}...")
        news = await get_company_news(symbol, "2025-01-01", "2025-01-08")
        print(f"   Found {len(news)} news articles")
        if news:
            print(f"   Latest: {news[0].get('headline', 'N/A')[:80]}...\n")

        # Test 4: Earnings Calendar
        print(f"4. Fetching earnings calendar...")
        earnings = await get_earnings_calendar("2025-01-01", "2025-01-31")
        earnings_count = len(earnings.get('earningsCalendar', []))
        print(f"   Found {earnings_count} earnings announcements\n")

        # Test 5: Basic Financials
        print(f"5. Fetching basic financials for {symbol}...")
        financials = await get_basic_financials(symbol)
        metrics = financials.get('metric', {})
        print(f"   P/E Ratio: {metrics.get('peNormalizedAnnual', 'N/A')}")
        print(f"   52-Week High: ${metrics.get('52WeekHigh', 'N/A')}")
        print(f"   52-Week Low: ${metrics.get('52WeekLow', 'N/A')}\n")

        # Test 6: Recommendation Trends
        print(f"6. Fetching recommendation trends for {symbol}...")
        recommendations = await get_recommendation_trends(symbol)
        if recommendations:
            latest = recommendations[0]
            print(f"   Period: {latest.get('period', 'N/A')}")
            print(f"   Buy: {latest.get('buy', 0)}, Hold: {latest.get('hold', 0)}, Sell: {latest.get('sell', 0)}\n")

        # Test 7: Institutional Ownership
        print(f"7. Fetching institutional ownership for {symbol}...")
        ownership = await get_institutional_ownership(symbol)
        ownership_data = ownership.get('data', [])
        print(f"   Found {len(ownership_data)} institutional holders")
        if ownership_data:
            top_holder = ownership_data[0]
            print(f"   Top Holder: {top_holder.get('name', 'N/A')}\n")

        # Test 8: Peers
        print(f"8. Fetching peer companies for {symbol}...")
        peers = await get_peers(symbol)
        print(f"   Peers: {', '.join(peers[:5])}\n")

        print(f"{'='*60}")
        print("All handler tests completed successfully!")
        print(f"{'='*60}\n")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())