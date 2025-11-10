"""
Test script to fetch all available data for Apple (AAPL) from Finnhub API
and store it in the database.
"""
import asyncio
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import (
    # Company Data
    get_company_profile,
    get_executives,
    get_peers,
    # Quotes & Market Data
    get_quote,
    # News
    get_company_news,
    # Financials
    get_basic_financials,
    get_financials_as_reported,
    # Estimates & Earnings
    get_revenue_estimates,
    get_eps_estimates,
    get_historical_earnings,
    # Recommendations
    get_recommendation_trends,
    get_price_target,
    # Insider & Institutional
    get_insider_transactions,
    get_institutional_ownership,
    get_fund_ownership,
    # Splits & Dividends
    get_dividends,
    get_splits,
)

from models import (
    CompanyProfile,
    CompanyExecutive,
    CompanyPeer,
    StockQuote,
    CompanyNews,
    BasicFinancials,
    FinancialReportData,
    RevenueEstimate,
    EpsEstimate,
    HistoricalEarnings,
    RecommendationTrend,
    PriceTarget,
    InsiderTransaction,
    InstitutionalOwnership,
    FundOwnership,
    Dividend,
    StockSplit,
)

from utils import save_to_db
from database.core import engine

load_dotenv()

SYMBOL = "AAPL"


async def test_company_profile():
    """Test fetching company profile and save to database."""
    print(f"\n{'='*60}")
    print("🏢 Testing Company Profile")
    print('='*60)
    try:
        data = await get_company_profile(SYMBOL)
        print(f"✅ Company: {data.get('name', 'N/A')}")
        print(f"   Industry: {data.get('finnhubIndustry', 'N/A')}")
        print(f"   Market Cap: ${data.get('marketCapitalization', 0):,.0f}M")
        print(f"   Country: {data.get('country', 'N/A')}")

        # Save to database
        if data:
            await save_to_db(CompanyProfile, data)
            print("   💾 Saved to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_executives():
    """Test fetching company executives and save to database."""
    print(f"\n{'='*60}")
    print("👥 Testing Company Executives")
    print('='*60)
    try:
        data = await get_executives(SYMBOL)
        executives = data.get('executive', [])
        print(f"✅ Found {len(executives)} executives")
        for exec in executives[:3]:  # Show first 3
            print(f"   - {exec.get('name', 'N/A')}: {exec.get('position', 'N/A')}")

        # Save to database
        if executives:
            # Add symbol to each executive
            for exec in executives:
                exec['symbol'] = SYMBOL
            await save_to_db(CompanyExecutive, executives)
            print(f"   💾 Saved {len(executives)} executives to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_peers():
    """Test fetching peer companies and save to database."""
    print(f"\n{'='*60}")
    print("🤝 Testing Peer Companies")
    print('='*60)
    try:
        data = await get_peers(SYMBOL)
        print(f"✅ Found {len(data)} peer companies")
        print(f"   Peers: {', '.join(data[:5])}")

        # Save to database
        if data:
            peers_data = [{'symbol': SYMBOL, 'peer_symbol': peer} for peer in data]
            await save_to_db(CompanyPeer, peers_data)
            print(f"   💾 Saved {len(peers_data)} peers to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_quote():
    """Test fetching real-time quote and save to database."""
    print(f"\n{'='*60}")
    print("💵 Testing Real-Time Quote")
    print('='*60)
    try:
        data = await get_quote(SYMBOL)
        print(f"✅ Current Price: ${data.get('c', 0):.2f}")
        print(f"   Change: {data.get('d', 0):.2f} ({data.get('dp', 0):.2f}%)")
        print(f"   High: ${data.get('h', 0):.2f} | Low: ${data.get('l', 0):.2f}")

        # Save to database
        if data:
            data['symbol'] = SYMBOL
            # Map API field names to model field names
            quote_data = {
                'symbol': SYMBOL,
                'current_price': data.get('c'),
                'change': data.get('d'),
                'percent_change': data.get('dp'),
                'high': data.get('h'),
                'low': data.get('l'),
                'open_price': data.get('o'),
                'previous_close': data.get('pc'),
                'timestamp': data.get('t'),
            }
            await save_to_db(StockQuote, quote_data)
            print("   💾 Saved to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_company_news():
    """Test fetching company news and save to database."""
    print(f"\n{'='*60}")
    print("📰 Testing Company News")
    print('='*60)
    try:
        # Get news from last 7 days
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        data = await get_company_news(SYMBOL, from_date, to_date)
        print(f"✅ Found {len(data)} news articles (last 7 days)")
        if data:
            print(f"   Latest: {data[0].get('headline', 'N/A')[:60]}...")

            # Save to database
            for article in data:
                article['symbol'] = SYMBOL
            await save_to_db(CompanyNews, data)
            print(f"   💾 Saved {len(data)} articles to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_basic_financials():
    """Test fetching basic financial metrics and save to database."""
    print(f"\n{'='*60}")
    print("💰 Testing Basic Financials")
    print('='*60)
    try:
        data = await get_basic_financials(SYMBOL)
        metrics = data.get('metric', {})
        print(f"✅ P/E Ratio: {metrics.get('peBasicExclExtraTTM', 'N/A')}")
        print(f"   52W High: ${metrics.get('52WeekHigh', 0):.2f}")
        print(f"   52W Low: ${metrics.get('52WeekLow', 0):.2f}")
        print(f"   Beta: {metrics.get('beta', 'N/A')}")

        # Save to database
        if metrics:
            financial_data = {
                'symbol': SYMBOL,
                'metrics': metrics,  # Store as JSON
                'series': data.get('series', {}),  # Store as JSON
            }
            await save_to_db(BasicFinancials, financial_data)
            print("   💾 Saved to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_financials_as_reported():
    """Test fetching financials as reported and save to database."""
    print(f"\n{'='*60}")
    print("📊 Testing Financials (As Reported)")
    print('='*60)
    try:
        # Test annual financials
        data = await get_financials_as_reported(SYMBOL, freq='annual')
        reports = data.get('data', [])
        print(f"✅ Found {len(reports)} annual reports")
        if reports:
            latest = reports[0]
            print(f"   Latest: {latest.get('year', 'N/A')} {latest.get('quarter', '')}")
            print(f"   Form: {latest.get('form', 'N/A')}")

            # Save to database
            for report in reports:
                report['symbol'] = SYMBOL
            await save_to_db(FinancialReportData, reports)
            print(f"   💾 Saved {len(reports)} reports to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_revenue_estimates():
    """Test fetching revenue estimates and save to database."""
    print(f"\n{'='*60}")
    print("📈 Testing Revenue Estimates")
    print('='*60)
    try:
        data = await get_revenue_estimates(SYMBOL)
        estimates = data.get('data', [])
        print(f"✅ Found {len(estimates)} revenue estimates")
        if estimates:
            latest = estimates[0]
            print(f"   Period: {latest.get('period', 'N/A')}")
            print(f"   Estimate: ${latest.get('revenueAvg', 0):,.0f}M")

            # Save to database
            for estimate in estimates:
                estimate['symbol'] = SYMBOL
            await save_to_db(RevenueEstimate, estimates)
            print(f"   💾 Saved {len(estimates)} estimates to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_eps_estimates():
    """Test fetching EPS estimates and save to database."""
    print(f"\n{'='*60}")
    print("📈 Testing EPS Estimates")
    print('='*60)
    try:
        data = await get_eps_estimates(SYMBOL)
        estimates = data.get('data', [])
        print(f"✅ Found {len(estimates)} EPS estimates")
        if estimates:
            latest = estimates[0]
            print(f"   Period: {latest.get('period', 'N/A')}")
            print(f"   Estimate: ${latest.get('epsAvg', 0):.2f}")

            # Save to database
            for estimate in estimates:
                estimate['symbol'] = SYMBOL
            await save_to_db(EpsEstimate, estimates)
            print(f"   💾 Saved {len(estimates)} estimates to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_historical_earnings():
    """Test fetching historical earnings and save to database."""
    print(f"\n{'='*60}")
    print("📊 Testing Historical Earnings")
    print('='*60)
    try:
        data = await get_historical_earnings(SYMBOL, limit=4)
        print(f"✅ Found {len(data)} earnings reports")
        if data:
            latest = data[0]
            print(f"   Latest: {latest.get('period', 'N/A')}")
            print(f"   Actual EPS: ${latest.get('actual', 0):.2f}")
            print(f"   Estimate EPS: ${latest.get('estimate', 0):.2f}")

            # Save to database
            for earning in data:
                earning['symbol'] = SYMBOL
            await save_to_db(HistoricalEarnings, data)
            print(f"   💾 Saved {len(data)} earnings to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_recommendation_trends():
    """Test fetching analyst recommendations and save to database."""
    print(f"\n{'='*60}")
    print("⭐ Testing Recommendation Trends")
    print('='*60)
    try:
        data = await get_recommendation_trends(SYMBOL)
        print(f"✅ Found {len(data)} recommendation periods")
        if data:
            latest = data[0]
            print(f"   Period: {latest.get('period', 'N/A')}")
            print(f"   Buy: {latest.get('buy', 0)} | Hold: {latest.get('hold', 0)} | Sell: {latest.get('sell', 0)}")

            # Save to database
            for rec in data:
                rec['symbol'] = SYMBOL
            await save_to_db(RecommendationTrend, data)
            print(f"   💾 Saved {len(data)} recommendations to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_price_target():
    """Test fetching price targets and save to database."""
    print(f"\n{'='*60}")
    print("🎯 Testing Price Target")
    print('='*60)
    try:
        data = await get_price_target(SYMBOL)
        print(f"✅ Target Price: ${data.get('targetMean', 0):.2f}")
        print(f"   High: ${data.get('targetHigh', 0):.2f} | Low: ${data.get('targetLow', 0):.2f}")
        print(f"   Last Updated: {data.get('lastUpdated', 'N/A')}")

        # Save to database
        if data:
            data['symbol'] = SYMBOL
            await save_to_db(PriceTarget, data)
            print("   💾 Saved to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None



async def test_insider_transactions():
    """Test fetching insider transactions and save to database."""
    print(f"\n{'='*60}")
    print("👤 Testing Insider Transactions")
    print('='*60)
    try:
        data = await get_insider_transactions(SYMBOL)
        transactions = data.get('data', [])
        print(f"✅ Found {len(transactions)} insider transactions")
        if transactions:
            latest = transactions[0]
            print(f"   Latest: {latest.get('name', 'N/A')}")
            print(f"   Transaction: {latest.get('transactionCode', 'N/A')} - {latest.get('share', 0)} shares")

            # Save to database
            await save_to_db(InsiderTransaction, transactions)
            print(f"   💾 Saved {len(transactions)} transactions to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_institutional_ownership():
    """Test fetching institutional ownership and save to database."""
    print(f"\n{'='*60}")
    print("🏦 Testing Institutional Ownership")
    print('='*60)
    try:
        # Get ownership from last 3 months
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        data = await get_institutional_ownership(SYMBOL, from_date, to_date)
        ownership = data.get('data', [])
        print(f"✅ Found {len(ownership)} institutional ownership records")
        if ownership:
            top = ownership[0]
            print(f"   Institution: {top.get('name', 'N/A')}")
            print(f"   Shares: {top.get('share', 0):,}")
            print(f"   Change: {top.get('change', 0):,}")

            # Save to database
            await save_to_db(InstitutionalOwnership, ownership)
            print(f"   💾 Saved {len(ownership)} ownership records to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_fund_ownership():
    """Test fetching fund ownership and save to database."""
    print(f"\n{'='*60}")
    print("💼 Testing Fund Ownership")
    print('='*60)
    try:
        data = await get_fund_ownership(SYMBOL, limit=5)
        ownership = data.get('data', [])
        print(f"✅ Found {len(ownership)} fund holders")
        if ownership:
            top = ownership[0]
            print(f"   Top Fund: {top.get('name', 'N/A')}")
            print(f"   Shares: {top.get('share', 0):,}")

            # Save to database
            await save_to_db(FundOwnership, ownership)
            print(f"   💾 Saved {len(ownership)} fund records to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_dividends():
    """Test fetching dividend history and save to database."""
    print(f"\n{'='*60}")
    print("💎 Testing Dividends")
    print('='*60)
    try:
        # Get dividends from last 2 years
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

        data = await get_dividends(SYMBOL, from_date, to_date)
        print(f"✅ Found {len(data)} dividend payments (last 2 years)")
        if data:
            latest = data[-1] if data else None
            if latest:
                print(f"   Latest: ${latest.get('amount', 0):.2f} on {latest.get('date', 'N/A')}")

            # Save to database
            for div in data:
                div['symbol'] = SYMBOL
            await save_to_db(Dividend, data)
            print(f"   💾 Saved {len(data)} dividends to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def test_splits():
    """Test fetching stock splits and save to database."""
    print(f"\n{'='*60}")
    print("✂️ Testing Stock Splits")
    print('='*60)
    try:
        # Get splits from last 10 years
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=3650)).strftime("%Y-%m-%d")

        data = await get_splits(SYMBOL, from_date, to_date)
        print(f"✅ Found {len(data)} stock splits (last 10 years)")
        if data:
            for split in data:
                print(f"   {split.get('date', 'N/A')}: {split.get('fromFactor', 0)}-for-{split.get('toFactor', 0)}")

            # Save to database
            for split in data:
                split['symbol'] = SYMBOL
            await save_to_db(StockSplit, data)
            print(f"   💾 Saved {len(data)} splits to database")

        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def run_all_tests():
    """Run all tests and collect results."""
    print("\n" + "="*60)
    print(f"🍎 TESTING ALL DATA ENDPOINTS FOR {SYMBOL}")
    print("="*60)

    # Start timing
    start_time = time.time()

    results = {}

    # Run all tests
    results['company_profile'] = await test_company_profile()
    results['executives'] = await test_executives()
    results['peers'] = await test_peers()
    results['quote'] = await test_quote()
    results['company_news'] = await test_company_news()
    results['basic_financials'] = await test_basic_financials()
    results['financials_as_reported'] = await test_financials_as_reported()
    results['revenue_estimates'] = await test_revenue_estimates()
    results['eps_estimates'] = await test_eps_estimates()
    results['historical_earnings'] = await test_historical_earnings()
    results['recommendation_trends'] = await test_recommendation_trends()
    results['price_target'] = await test_price_target()
    results['insider_transactions'] = await test_insider_transactions()
    results['institutional_ownership'] = await test_institutional_ownership()
    results['fund_ownership'] = await test_fund_ownership()
    results['dividends'] = await test_dividends()
    results['splits'] = await test_splits()

    # End timing
    end_time = time.time()
    total_time = end_time - start_time

    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    successful = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    print(f"\n⏱️  Time taken: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"📈 Average time per endpoint: {total_time/total:.2f} seconds")

    # List failed tests
    failed_tests = [k for k, v in results.items() if v is None]
    if failed_tests:
        print(f"\n⚠️  Failed tests:")
        for test in failed_tests:
            print(f"   - {test}")

    # Save results to file
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{SYMBOL}_test_results.json"

    with open(output_file, 'w') as f:
        # Convert results to JSON-serializable format
        json_results = {k: v for k, v in results.items() if v is not None}
        json.dump(json_results, f, indent=2, default=str)

    print(f"\n💾 Full results saved to: {output_file}")

    return results


async def main():
    """Main entry point."""
    try:
        await run_all_tests()
    finally:
        # Cleanup database connection
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
