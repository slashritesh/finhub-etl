# Finnhub API Handlers Documentation

This document provides a comprehensive list of all API handlers available in the `finhub_etl` package.

**Reference:** [Finnhub API Documentation](https://finnhub.io/docs/api)

## Table of Contents

1. [Overview](#overview)
2. [Handler Classes](#handler-classes)
   - [AnalystHandlers](#1-analysthandlers)
   - [CompanyHandlers](#2-companyhandlers)
   - [EarningsHandlers](#3-earningshandlers)
   - [FinancialsHandlers](#4-financialshandlers)
   - [MarketHandlers](#5-markethandlers)
   - [NewsHandlers](#6-newshandlers)
   - [OwnershipHandlers](#7-ownershiphandlers)
   - [TradingHandlers](#8-tradinghandlers)
3. [Usage Examples](#usage-examples)

## Overview

The handlers package provides organized, async-compatible wrappers for all Finnhub API endpoints. There are:

- **8 Handler Classes**
- **41 Handler Methods**
- **All methods are async**
- **Complete endpoint coverage from endpoints.json**

### Unified Handler Interface

```python
from finhub_etl.config.finhub import api_client
from finhub_etl.config.handlers import FinnhubHandlers

handlers = FinnhubHandlers(api_client)

# Access any handler category
await handlers.analyst.get_recommendation_trends("AAPL")
await handlers.company.get_company_profile2("AAPL")
await handlers.market.get_quote("AAPL")
```

---

## Handler Classes

### 1. AnalystHandlers

**File:** `src/finhub_etl/config/handlers/analyst.py`

Provides access to analyst research data including recommendations, price targets, and estimates.

**Total Methods:** 7

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_recommendation_trends(symbol)` | `/stock/recommendation` | Get analyst recommendation trends (buy, hold, sell counts) |
| `get_price_target(symbol)` | `/stock/price-target` | Get price target consensus (high, low, average, median) |
| `get_upgrade_downgrade(symbol, from_date, to_date)` | `/stock/upgrade-downgrade` | Get analyst upgrades and downgrades |
| `get_revenue_estimate(symbol, freq)` | `/stock/revenue-estimate` | Get revenue estimates (annual or quarterly) |
| `get_eps_estimate(symbol, freq)` | `/stock/eps-estimate` | Get EPS estimates (annual or quarterly) |
| `get_ebitda_estimate(symbol, freq)` | `/stock/ebitda-estimate` | Get EBITDA estimates (annual or quarterly) |
| `get_ebit_estimate(symbol, freq)` | `/stock/ebit-estimate` | Get EBIT estimates (annual or quarterly) |

**Example:**
```python
# Get analyst recommendations
recommendations = await handlers.analyst.get_recommendation_trends("AAPL")

# Get EPS estimates
eps = await handlers.analyst.get_eps_estimate("AAPL", freq="quarterly")
```

---

### 2. CompanyHandlers

**File:** `src/finhub_etl/config/handlers/company.py`

Provides access to company information, profiles, executives, and corporate data.

**Total Methods:** 8

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_company_profile(symbol)` | `/stock/profile` | Get company profile (v1) |
| `get_company_profile2(symbol)` | `/stock/profile2` | Get company profile v2 (recommended) |
| `get_company_peers(symbol)` | `/stock/peers` | Get peer companies in same industry |
| `get_executive(symbol)` | `/stock/executive` | Get executive compensation and information |
| `get_historical_employee_count(symbol)` | `/stock/historical-employee-count` | Get historical employee count data |
| `get_filings(symbol, from_date, to_date, form)` | `/stock/filings` | Get SEC filings (10-K, 10-Q, etc.) |
| `get_price_metrics(symbol, date)` | `/stock/price-metric` | Get price metrics (52-week high/low, beta, MA) |
| `get_historical_market_cap(symbol, from_date, to_date)` | `/stock/historical-market-cap` | Get historical market capitalization |

**Example:**
```python
# Get company profile (v2 recommended)
profile = await handlers.company.get_company_profile2("AAPL")

# Get SEC filings
filings = await handlers.company.get_filings("AAPL", "2024-01-01", "2024-12-31", form="10-K")

# Get historical market cap
market_cap = await handlers.company.get_historical_market_cap("AAPL")
```

---

### 3. EarningsHandlers

**File:** `src/finhub_etl/config/handlers/earnings.py`

Provides access to earnings data and calendars.

**Total Methods:** 2

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_earnings(symbol, limit)` | `/stock/earnings` | Get historical quarterly earnings surprise data |
| `get_earnings_calendar(from_date, to_date, symbol, international)` | `/calendar/earnings` | Get earnings calendar for date range |

**Example:**
```python
# Get earnings history
earnings = await handlers.earnings.get_earnings("AAPL", limit=10)

# Get upcoming earnings
calendar = await handlers.earnings.get_earnings_calendar("2024-01-01", "2024-03-31")
```

---

### 4. FinancialsHandlers

**File:** `src/finhub_etl/config/handlers/financials.py`

Provides access to financial statements, metrics, and sector data.

**Total Methods:** 5

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_basic_financials(symbol, metric)` | `/stock/metric` | Get basic financial metrics (P/E, margins, etc.) |
| `get_financials(symbol, statement, freq)` | `/stock/financials` | Get standardized financial statements (BS, IC, CF) |
| `get_financials_reported(symbol, freq)` | `/stock/financials-reported` | Get as-reported financial statements |
| `get_sector_metrics(region)` | `/sector/metrics` | Get sector performance and valuation metrics |
| `get_earnings_quality_score(symbol, freq)` | `/stock/earnings-quality-score` | Get earnings quality score |

**Statement Types:**
- `bs` - Balance Sheet
- `ic` - Income Statement
- `cf` - Cash Flow Statement

**Example:**
```python
# Get basic financials
metrics = await handlers.financials.get_basic_financials("AAPL", metric="all")

# Get income statement (annual)
income_stmt = await handlers.financials.get_financials("AAPL", statement="ic", freq="annual")

# Get sector metrics
sector_data = await handlers.financials.get_sector_metrics(region="us")
```

---

### 5. MarketHandlers

**File:** `src/finhub_etl/config/handlers/market.py`

Provides access to market data, quotes, candles, and technical indicators.

**Total Methods:** 7

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_symbol_lookup(query)` | `/search` | Search for symbols by company name or ticker |
| `get_stock_symbols(exchange, mic, security_type, currency)` | `/stock/symbol` | Get list of supported stocks for exchange |
| `get_market_status(exchange)` | `/stock/market-status` | Get current market status (open/closed) |
| `get_market_holiday(exchange)` | `/stock/market-holiday` | Get market holidays and trading hours |
| `get_quote(symbol)` | `/quote` | Get real-time quote data |
| `get_candles(symbol, resolution, from_timestamp, to_timestamp)` | `/stock/candle` | Get OHLCV candlestick data |
| `get_technical_indicators(symbol, resolution, from_timestamp, to_timestamp, indicator, **fields)` | `/indicator` | Get technical indicator values (RSI, MACD, SMA, etc.) |

**Candle Resolutions:**
- `1`, `5`, `15`, `30`, `60` - Minutes
- `D` - Daily
- `W` - Weekly
- `M` - Monthly

**Example:**
```python
# Get real-time quote
quote = await handlers.market.get_quote("AAPL")

# Get daily candles (UNIX timestamps)
candles = await handlers.market.get_candles("AAPL", "D", 1609459200, 1640995200)

# Get RSI indicator
rsi = await handlers.market.get_technical_indicators(
    "AAPL", "D", 1609459200, 1640995200, "rsi", timeperiod=14
)

# Search for symbols
results = await handlers.market.get_symbol_lookup("Apple")
```

---

### 6. NewsHandlers

**File:** `src/finhub_etl/config/handlers/news.py`

Provides access to news articles and press releases.

**Total Methods:** 3

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_general_news(category, min_id)` | `/news` | Get general market news by category |
| `get_company_news(symbol, from_date, to_date)` | `/company-news` | Get company-specific news |
| `get_press_releases(symbol, from_date, to_date)` | `/press-releases2` | Get company press releases |

**News Categories:**
- `general` - General market news
- `forex` - Forex news
- `crypto` - Cryptocurrency news
- `merger` - Merger & acquisition news

**Example:**
```python
# Get general market news
news = await handlers.news.get_general_news(category="general")

# Get company news for date range
company_news = await handlers.news.get_company_news("AAPL", "2024-01-01", "2024-12-31")

# Get press releases
press = await handlers.news.get_press_releases("AAPL")
```

---

### 7. OwnershipHandlers

**File:** `src/finhub_etl/config/handlers/ownership.py`

Provides access to ownership, institutional holdings, and insider transaction data.

**Total Methods:** 6

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_ownership(symbol, limit)` | `/stock/ownership` | Get shareholder ownership breakdown |
| `get_fund_ownership(symbol, limit)` | `/stock/fund-ownership` | Get mutual fund ownership data |
| `get_institutional_profile(cik, isin)` | `/institutional/profile` | Get institutional investor profile |
| `get_institutional_portfolio(cik, from_date, to_date)` | `/institutional/portfolio` | Get institutional portfolio holdings |
| `get_institutional_ownership(symbol, cusip, from_date, to_date)` | `/institutional/ownership` | Get institutional ownership for a stock |
| `get_insider_transactions(symbol, from_date, to_date)` | `/stock/insider-transactions` | Get insider buy/sell transactions |

**Example:**
```python
# Get ownership breakdown
ownership = await handlers.ownership.get_ownership("AAPL")

# Get institutional ownership
inst_ownership = await handlers.ownership.get_institutional_ownership("AAPL")

# Get insider transactions
insider = await handlers.ownership.get_insider_transactions("AAPL", "2024-01-01", "2024-12-31")

# Get institutional portfolio by CIK
portfolio = await handlers.ownership.get_institutional_portfolio(cik="0001067983")
```

---

### 8. TradingHandlers

**File:** `src/finhub_etl/config/handlers/trading.py`

Provides access to trading-related events: IPOs, dividends, and stock splits.

**Total Methods:** 3

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_ipo_calendar(from_date, to_date)` | `/calendar/ipo` | Get IPO calendar for date range |
| `get_dividends(symbol, from_date, to_date)` | `/stock/dividend` | Get dividend events |
| `get_splits(symbol, from_date, to_date)` | `/stock/split` | Get stock split events |

**Example:**
```python
# Get IPO calendar
ipos = await handlers.trading.get_ipo_calendar("2024-01-01", "2024-12-31")

# Get dividend history
dividends = await handlers.trading.get_dividends("AAPL", "2024-01-01", "2024-12-31")

# Get stock splits
splits = await handlers.trading.get_splits("AAPL", "2020-01-01", "2024-12-31")
```

---

## Usage Examples

### Complete Setup

```python
import asyncio
from finhub_etl.config.finhub import api_client
from finhub_etl.config.handlers import FinnhubHandlers

async def main():
    # Initialize handlers
    handlers = FinnhubHandlers(api_client)

    # Get company profile
    profile = await handlers.company.get_company_profile2("AAPL")
    print(f"Company: {profile['name']}")

    # Get real-time quote
    quote = await handlers.market.get_quote("AAPL")
    print(f"Current Price: ${quote['c']}")

    # Get analyst recommendations
    recs = await handlers.analyst.get_recommendation_trends("AAPL")
    print(f"Recommendations: {recs}")

    # Get recent earnings
    earnings = await handlers.earnings.get_earnings("AAPL", limit=4)
    print(f"Earnings: {earnings}")

    # Get financial statements
    financials = await handlers.financials.get_financials("AAPL", "ic", "annual")
    print(f"Income Statement: {financials}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Individual Handler Usage

```python
# Use individual handler classes if needed
from finhub_etl.config.finhub import api_client
from finhub_etl.config.handlers import CompanyHandlers, MarketHandlers

company_handler = CompanyHandlers(api_client)
market_handler = MarketHandlers(api_client)

# Use handlers
profile = await company_handler.get_company_profile2("AAPL")
quote = await market_handler.get_quote("AAPL")
```

### Error Handling

```python
import httpx

try:
    profile = await handlers.company.get_company_profile2("INVALID")
except httpx.HTTPStatusError as e:
    print(f"HTTP Error: {e.response.status_code}")
except Exception as e:
    print(f"Error: {str(e)}")
```

---

## Summary Statistics

| Category | Handler Class | Methods | Key Endpoints |
|----------|--------------|---------|---------------|
| **Analyst** | AnalystHandlers | 7 | Recommendations, Estimates, Price Targets |
| **Company** | CompanyHandlers | 8 | Profile, Executives, Filings, Metrics |
| **Earnings** | EarningsHandlers | 2 | Earnings Data, Calendar |
| **Financials** | FinancialsHandlers | 5 | Statements, Metrics, Sector Data |
| **Market** | MarketHandlers | 7 | Quotes, Candles, Symbols, Indicators |
| **News** | NewsHandlers | 3 | News, Press Releases |
| **Ownership** | OwnershipHandlers | 6 | Ownership, Institutional, Insider |
| **Trading** | TradingHandlers | 3 | IPO, Dividends, Splits |
| **TOTAL** | **8 Classes** | **41 Methods** | **42 Unique Endpoints** |

---

## Notes

- All methods are **async** and must be awaited
- Dates should be in **YYYY-MM-DD** format
- Timestamps for candles are **UNIX timestamps in seconds**
- All handlers use the same `FinnhubAPIClient` instance
- API responses are returned as Python dictionaries or lists
- HTTP errors are raised as `httpx.HTTPStatusError` exceptions

For more details, see the [Finnhub API Documentation](https://finnhub.io/docs/api).
