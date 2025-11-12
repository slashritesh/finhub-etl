# Finhub ETL - Database Models Documentation

This document provides a comprehensive overview of all SQLModel classes used in the finhub-etl project. These models map to database tables and represent various financial data entities from the Finnhub API.

## Table of Contents

1. [Overview](#overview)
2. [Model Statistics](#model-statistics)
3. [Model Categories](#model-categories)
4. [Model Reference](#model-reference)

---

## Overview

The finhub-etl project uses SQLModel for ORM (Object-Relational Mapping) with MySQL database. All models inherit from SQLModel and are designed to store financial market data from the Finnhub API.

**Key Features:**
- Async database operations using aiomysql
- Automatic table creation via Alembic migrations
- Type-safe models with Pydantic validation
- Direct mapping to Finnhub API responses

---

## Model Statistics

**Total Models:** 41

**Model Categories:**
- Market Data: 5 models
- Company Information: 10 models
- Financial Statements: 8 models
- Analyst Coverage: 7 models
- Ownership Data: 5 models
- News & Press: 3 models
- Trading Events: 3 models

---

## Model Categories

### 1. Market Data Models (5)

Models related to stock symbols, quotes, and market status.

#### 1.1 StockSymbol
**File:** `src/finhub_etl/models/symbols.py`
**Handler:** `market.get_stock_symbols`, `market.get_symbol_lookup`
**Endpoint:** `/stock/symbol`, `/search`

Stock symbol information including exchange, currency, and security type.

**Key Fields:**
- `symbol`: Stock ticker symbol
- `description`: Company name
- `displaySymbol`: Display format of symbol
- `type`: Security type (stock, ETF, etc.)
- `mic`: Market Identifier Code
- `figi`: Financial Instrument Global Identifier

---

#### 1.2 MatchedStock
**File:** `src/finhub_etl/models/matched_stock.py`
**Handler:** `market.get_symbol_lookup`
**Endpoint:** `/search`

Search results for stock symbol lookups.

**Key Fields:**
- `symbol`: Stock ticker
- `description`: Company description
- `displaySymbol`: Display symbol
- `type`: Security type

---

#### 1.3 RealtimeQuote
**File:** `src/finhub_etl/models/quote.py`
**Handler:** `market.get_quote`
**Endpoint:** `/quote`

Real-time stock price quotes.

**Key Fields:**
- `symbol`: Stock ticker
- `c`: Current price
- `h`: High price of the day
- `l`: Low price of the day
- `o`: Open price
- `pc`: Previous close price
- `t`: Timestamp

---

#### 1.4 MarketStatus
**File:** `src/finhub_etl/models/market_info.py`
**Handler:** `market.get_market_status`
**Endpoint:** `/stock/market-status`

Current market open/close status.

**Key Fields:**
- `exchange`: Exchange code
- `holiday`: Holiday name (if closed)
- `isOpen`: Market open status
- `session`: Trading session
- `timezone`: Market timezone

---

#### 1.5 MarketHoliday
**File:** `src/finhub_etl/models/market_info.py`
**Handler:** `market.get_market_holiday`
**Endpoint:** `/stock/market-holiday`

Market holiday calendar.

**Key Fields:**
- `exchange`: Exchange code
- `data`: List of holiday dates
- `timezone`: Market timezone

---

### 2. Company Information Models (10)

Models containing company profile, executives, peers, and operational data.

#### 2.1 CompanyProfile
**File:** `src/finhub_etl/models/company_profile.py`
**Handler:** `company.get_company_profile`
**Endpoint:** `/stock/profile`

Basic company profile information (legacy).

**Key Fields:**
- `symbol`: Stock ticker
- `name`: Company name
- `address`: Company address
- `city`, `state`, `country`
- `phone`, `weburl`
- `marketCapitalization`
- `shareOutstanding`

---

#### 2.2 CompanyProfile2
**File:** `src/finhub_etl/models/company_profile.py`
**Handler:** `company.get_company_profile2`
**Endpoint:** `/stock/profile2`

Enhanced company profile (recommended version).

**Key Fields:**
- `symbol`: Stock ticker
- `name`: Company name
- `ticker`: Stock ticker
- `exchange`: Exchange code
- `industry`, `sector`
- `marketCapitalization`
- `logo`: Company logo URL
- `ipo`: IPO date
- `finnhubIndustry`: Finnhub industry classification

---

#### 2.3 CompanyPeer
**File:** `src/finhub_etl/models/company_peers.py`
**Handler:** `company.get_company_peers`
**Endpoint:** `/stock/peers`

List of peer companies.

**Key Fields:**
- `symbol`: Stock ticker
- `peer`: Peer company symbol

---

#### 2.4 CompanyExecutive
**File:** `src/finhub_etl/models/executive.py`
**Handler:** `company.get_executive`
**Endpoint:** `/stock/executive`

Company executive information.

**Key Fields:**
- `symbol`: Stock ticker
- `name`: Executive name
- `age`: Executive age
- `title`: Job title
- `since`: Start date
- `compensation`: Total compensation
- `currency`: Compensation currency

---

#### 2.5 HistoricalEmployeeCount
**File:** `src/finhub_etl/models/employee_count.py`
**Handler:** `company.get_historical_employee_count`
**Endpoint:** `/stock/historical-employee-count`

Historical employee headcount data.

**Key Fields:**
- `symbol`: Stock ticker
- `employeeCount`: Number of employees
- `periodDate`: Report date
- `filingDate`: Filing date

---

#### 2.6 CompanyFiling
**File:** `src/finhub_etl/models/filing.py`
**Handler:** `company.get_filings`
**Endpoint:** `/stock/filings`

SEC filings (10-K, 10-Q, 8-K, etc.).

**Key Fields:**
- `symbol`: Stock ticker
- `cik`: CIK number
- `form`: Filing form type
- `filedDate`: Filing date
- `acceptedDate`: Acceptance date
- `reportUrl`: URL to filing
- `filingUrl`: URL to filing document

---

#### 2.7 PriceMetrics
**File:** `src/finhub_etl/models/price_metrics.py`
**Handler:** `company.get_price_metrics`
**Endpoint:** `/stock/price-metric`

Price-based metrics and ratios.

**Key Fields:**
- `symbol`: Stock ticker
- `52WeekHigh`, `52WeekLow`
- `beta`: Beta coefficient
- `marketCapitalization`
- `peRatio`: P/E ratio
- `pbRatio`: P/B ratio

---

#### 2.8 HistoricalMarketCap
**File:** `src/finhub_etl/models/historical_mcap.py`
**Handler:** `company.get_historical_market_cap`
**Endpoint:** `/stock/historical-market-cap`

Historical market capitalization data.

**Key Fields:**
- `symbol`: Stock ticker
- `atDate`: Date
- `marketCapitalization`: Market cap value

---

#### 2.9 CandlestickData
**File:** `src/finhub_etl/models/candle.py`
**Handler:** `market.get_candles`
**Endpoint:** `/stock/candle`

OHLCV (Open, High, Low, Close, Volume) candlestick data.

**Key Fields:**
- `symbol`: Stock ticker
- `timestamp`: Unix timestamp
- `open`: Open price
- `high`: High price
- `low`: Low price
- `close`: Close price
- `volume`: Trading volume
- `resolution`: Candle resolution (1, 5, 15, 30, 60, D, W, M)

---

#### 2.10 TechnicalIndicator
**File:** `src/finhub_etl/models/technical_indicator.py`
**Handler:** `market.get_technical_indicators`
**Endpoint:** `/indicator`

Technical indicator calculations (RSI, MACD, EMA, SMA, etc.).

**Key Fields:**
- `symbol`: Stock ticker
- `indicator`: Indicator name
- `timestamp`: Unix timestamp
- `value`: Indicator value
- `resolution`: Time resolution

---

### 3. Financial Statements Models (8)

Models for financial statements, metrics, and earnings.

#### 3.1 BasicFinancials
**File:** `src/finhub_etl/models/financials.py`
**Handler:** `financials.get_basic_financials`
**Endpoint:** `/stock/metric`

Basic financial metrics and ratios.

**Key Fields:**
- `symbol`: Stock ticker
- `metric`: Metric name
- `value`: Metric value
- `annual`, `quarterly`: Aggregation type

---

#### 3.2 CompanyFinancials
**File:** `src/finhub_etl/models/financials.py`
**Handler:** `financials.get_financials`
**Endpoint:** `/stock/financials`

Standardized financial statements (balance sheet, income statement, cash flow).

**Key Fields:**
- `symbol`: Stock ticker
- `statement`: Statement type (bs, ic, cf)
- `cik`: CIK number
- `year`, `quarter`: Period
- `accessNumber`: SEC access number
- `financials`: JSON data

---

#### 3.3 ReportedFinancials
**File:** `src/finhub_etl/models/financials.py`
**Handler:** `financials.get_financials_reported`
**Endpoint:** `/stock/financials-reported`

As-reported financial statements from SEC filings.

**Key Fields:**
- `symbol`: Stock ticker
- `cik`: CIK number
- `year`, `quarter`: Period
- `form`: Filing form type
- `startDate`, `endDate`: Period dates
- `filedDate`: Filing date
- `report`: JSON report data

---

#### 3.4 SectorMetrics
**File:** `src/finhub_etl/models/sector_metrics.py`
**Handler:** `financials.get_sector_metrics`
**Endpoint:** `/sector/metrics`

Sector-level aggregated metrics.

**Key Fields:**
- `region`: Region code
- `sector`: Sector name
- `peRatio`, `pbRatio`: Valuation ratios
- `dividendYield`: Dividend yield

---

#### 3.5 EarningsData
**File:** `src/finhub_etl/models/earnings.py`
**Handler:** `earnings.get_earnings`
**Endpoint:** `/stock/earnings`

Historical earnings results.

**Key Fields:**
- `symbol`: Stock ticker
- `actual`: Actual EPS
- `estimate`: Estimated EPS
- `period`: Reporting period
- `quarter`: Quarter number
- `year`: Year
- `surprise`: Earnings surprise
- `surprisePercent`: Surprise percentage

---

#### 3.6 EarningsCalendar
**File:** `src/finhub_etl/models/earnings.py`
**Handler:** `earnings.get_earnings_calendar`
**Endpoint:** `/calendar/earnings`

Upcoming and past earnings announcements.

**Key Fields:**
- `symbol`: Stock ticker
- `date`: Earnings date
- `epsActual`: Actual EPS
- `epsEstimate`: Estimated EPS
- `hour`: Time of announcement
- `quarter`, `year`: Period
- `revenueActual`, `revenueEstimate`

---

#### 3.7 EarningsQualityScore
**File:** `src/finhub_etl/models/earnings_quality.py`
**Handler:** `financials.get_earnings_quality_score`
**Endpoint:** `/stock/earnings-quality-score`

Earnings quality scoring metrics.

**Key Fields:**
- `symbol`: Stock ticker
- `freq`: Frequency (annual/quarterly)
- `period`: Period date
- `score`: Quality score
- `roa`: Return on Assets
- `accruals`: Accruals ratio

---

#### 3.8 Dividend
**File:** `src/finhub_etl/models/dividend.py`
**Handler:** `trading.get_dividends`
**Endpoint:** `/stock/dividend`

Dividend payment history.

**Key Fields:**
- `symbol`: Stock ticker
- `date`: Payment date
- `amount`: Dividend amount
- `adjustedAmount`: Adjusted amount
- `currency`: Payment currency
- `declarationDate`: Declaration date
- `exDate`: Ex-dividend date
- `payDate`: Payment date
- `recordDate`: Record date

---

### 4. Analyst Coverage Models (7)

Models for analyst ratings, estimates, and price targets.

#### 4.1 AnalystRecommendation
**File:** `src/finhub_etl/models/analyst.py`
**Handler:** `analyst.get_recommendation_trends`
**Endpoint:** `/stock/recommendation`

Analyst recommendation trends.

**Key Fields:**
- `symbol`: Stock ticker
- `period`: Date period
- `buy`: Number of buy ratings
- `hold`: Number of hold ratings
- `sell`: Number of sell ratings
- `strongBuy`: Number of strong buy ratings
- `strongSell`: Number of strong sell ratings

---

#### 4.2 PriceTarget
**File:** `src/finhub_etl/models/analyst.py`
**Handler:** `analyst.get_price_target`
**Endpoint:** `/stock/price-target`

Analyst price targets.

**Key Fields:**
- `symbol`: Stock ticker
- `targetHigh`: Highest price target
- `targetLow`: Lowest price target
- `targetMean`: Average price target
- `targetMedian`: Median price target
- `lastUpdated`: Last update date

---

#### 4.3 UpgradeDowngrade
**File:** `src/finhub_etl/models/analyst.py`
**Handler:** `analyst.get_upgrade_downgrade`
**Endpoint:** `/stock/upgrade-downgrade`

Analyst rating changes.

**Key Fields:**
- `symbol`: Stock ticker
- `gradeTime`: Time of rating change
- `company`: Analyst firm name
- `fromGrade`: Previous rating
- `toGrade`: New rating
- `action`: Action type (upgrade/downgrade/init)

---

#### 4.4 RevenueEstimate
**File:** `src/finhub_etl/models/estimates.py`
**Handler:** `analyst.get_revenue_estimate`
**Endpoint:** `/stock/revenue-estimate`

Analyst revenue estimates.

**Key Fields:**
- `symbol`: Stock ticker
- `period`: Period date
- `revenueAvg`: Average estimate
- `revenueHigh`: Highest estimate
- `revenueLow`: Lowest estimate
- `numberAnalysts`: Number of analysts

---

#### 4.5 EpsEstimate
**File:** `src/finhub_etl/models/estimates.py`
**Handler:** `analyst.get_eps_estimate`
**Endpoint:** `/stock/eps-estimate`

Analyst EPS estimates.

**Key Fields:**
- `symbol`: Stock ticker
- `period`: Period date
- `epsAvg`: Average EPS estimate
- `epsHigh`: Highest estimate
- `epsLow`: Lowest estimate
- `numberAnalysts`: Number of analysts

---

#### 4.6 EbitdaEstimate
**File:** `src/finhub_etl/models/estimates.py`
**Handler:** `analyst.get_ebitda_estimate`
**Endpoint:** `/stock/ebitda-estimate`

Analyst EBITDA estimates.

**Key Fields:**
- `symbol`: Stock ticker
- `period`: Period date
- `ebitdaAvg`: Average EBITDA estimate
- `ebitdaHigh`: Highest estimate
- `ebitdaLow`: Lowest estimate
- `numberAnalysts`: Number of analysts

---

#### 4.7 EbitEstimate
**File:** `src/finhub_etl/models/estimates.py`
**Handler:** `analyst.get_ebit_estimate`
**Endpoint:** `/stock/ebit-estimate`

Analyst EBIT estimates.

**Key Fields:**
- `symbol`: Stock ticker
- `period`: Period date
- `ebitAvg`: Average EBIT estimate
- `ebitHigh`: Highest estimate
- `ebitLow`: Lowest estimate
- `numberAnalysts`: Number of analysts

---

### 5. Ownership Data Models (5)

Models tracking institutional, fund, and insider ownership.

#### 5.1 CompanyOwnership
**File:** `src/finhub_etl/models/ownership.py`
**Handler:** `ownership.get_ownership`
**Endpoint:** `/stock/ownership`

Ownership breakdown by investor type.

**Key Fields:**
- `symbol`: Stock ticker
- `investorName`: Investor name
- `change`: Change in holdings
- `filingDate`: Filing date
- `portfolioPercent`: Percentage of portfolio
- `share`: Number of shares
- `value`: Dollar value

---

#### 5.2 FundOwnership
**File:** `src/finhub_etl/models/ownership.py`
**Handler:** `ownership.get_fund_ownership`
**Endpoint:** `/stock/fund-ownership`

Mutual fund ownership data.

**Key Fields:**
- `symbol`: Stock ticker
- `name`: Fund name
- `change`: Change in holdings
- `filingDate`: Filing date
- `portfolioPercent`: Percentage of fund
- `share`: Number of shares
- `value`: Dollar value

---

#### 5.3 InstitutionalOwnership
**File:** `src/finhub_etl/models/ownership.py`
**Handler:** `ownership.get_institutional_ownership`
**Endpoint:** `/institutional/ownership`

Institutional ownership data.

**Key Fields:**
- `symbol`: Stock ticker
- `cik`: Institution CIK
- `name`: Institution name
- `change`: Change in holdings
- `filingDate`: Filing date
- `share`: Number of shares
- `value`: Dollar value

---

#### 5.4 InstitutionalProfile
**File:** `src/finhub_etl/models/institutional.py`
**Handler:** `ownership.get_institutional_profile`
**Endpoint:** `/institutional/profile`

Institutional investor profile.

**Key Fields:**
- `cik`: CIK number
- `name`: Institution name
- `manager`: Manager name
- `profile`: Profile details
- `numberOfHoldings`: Number of holdings
- `totalValue`: Total portfolio value

---

#### 5.5 InstitutionalPortfolio
**File:** `src/finhub_etl/models/institutional.py`
**Handler:** `ownership.get_institutional_portfolio`
**Endpoint:** `/institutional/portfolio`

Institutional portfolio holdings.

**Key Fields:**
- `cik`: Institution CIK
- `symbol`: Stock ticker
- `cusip`: CUSIP identifier
- `reportDate`: Report date
- `change`: Change in position
- `share`: Number of shares
- `value`: Dollar value

---

#### 5.6 InsiderTransaction
**File:** `src/finhub_etl/models/insider_transaction.py`
**Handler:** `ownership.get_insider_transactions`
**Endpoint:** `/stock/insider-transactions`

Insider trading transactions.

**Key Fields:**
- `symbol`: Stock ticker
- `name`: Insider name
- `share`: Number of shares traded
- `change`: Change in holdings
- `filingDate`: Filing date
- `transactionDate`: Transaction date
- `transactionCode`: Transaction type code
- `transactionPrice`: Transaction price

---

### 6. News & Press Models (3)

Models for news articles and press releases.

#### 6.1 GeneralNews
**File:** `src/finhub_etl/models/general_news.py`
**Handler:** `news.get_general_news`
**Endpoint:** `/news`

General market news articles.

**Key Fields:**
- `category`: News category
- `datetime`: Publication timestamp
- `headline`: Article headline
- `id`: Article ID
- `image`: Image URL
- `related`: Related symbols
- `source`: News source
- `summary`: Article summary
- `url`: Article URL

---

#### 6.2 CompanyNews
**File:** `src/finhub_etl/models/company_news.py`
**Handler:** `news.get_company_news`
**Endpoint:** `/company-news`

Company-specific news articles.

**Key Fields:**
- `symbol`: Stock ticker
- `datetime`: Publication timestamp
- `headline`: Article headline
- `id`: Article ID
- `image`: Image URL
- `related`: Related symbols
- `source`: News source
- `summary`: Article summary
- `url`: Article URL

---

#### 6.3 PressRelease
**File:** `src/finhub_etl/models/press_release.py`
**Handler:** `news.get_press_releases`
**Endpoint:** `/press-releases2`

Company press releases.

**Key Fields:**
- `symbol`: Stock ticker
- `datetime`: Publication timestamp
- `headline`: Press release title
- `id`: Press release ID
- `url`: Press release URL

---

### 7. Trading Events Models (3)

Models for IPOs, stock splits, and other corporate actions.

#### 7.1 IpoCalendar
**File:** `src/finhub_etl/models/ipo_calendar.py`
**Handler:** `trading.get_ipo_calendar`
**Endpoint:** `/calendar/ipo`

IPO calendar and pricing information.

**Key Fields:**
- `symbol`: Stock ticker
- `date`: IPO date
- `name`: Company name
- `exchange`: Exchange code
- `numberOfShares`: Number of shares
- `price`: IPO price
- `totalSharesValue`: Total value
- `status`: IPO status

---

#### 7.2 StockSplit
**File:** `src/finhub_etl/models/stock_split.py`
**Handler:** `trading.get_splits`
**Endpoint:** `/stock/split`

Stock split history.

**Key Fields:**
- `symbol`: Stock ticker
- `date`: Split date
- `fromFactor`: Split from factor
- `toFactor`: Split to factor

---

#### 7.3 Dividend
**File:** `src/finhub_etl/models/dividend.py`
**Handler:** `trading.get_dividends`
**Endpoint:** `/stock/dividend`

Dividend payment history (also listed under Financials).

---

## Model Reference

### Quick Reference Table

| # | Model Name | Category | Handler Module | Primary Key Field |
|---|---|---|---|---|
| 1 | StockSymbol | Market Data | market | symbol |
| 2 | MatchedStock | Market Data | market | symbol |
| 3 | RealtimeQuote | Market Data | market | symbol |
| 4 | MarketStatus | Market Data | market | exchange |
| 5 | MarketHoliday | Market Data | market | exchange |
| 6 | CompanyProfile | Company Info | company | symbol |
| 7 | CompanyProfile2 | Company Info | company | symbol |
| 8 | CompanyPeer | Company Info | company | symbol + peer |
| 9 | CompanyExecutive | Company Info | company | symbol + name |
| 10 | HistoricalEmployeeCount | Company Info | company | symbol + periodDate |
| 11 | CompanyFiling | Company Info | company | symbol + acceptedDate |
| 12 | PriceMetrics | Company Info | company | symbol + date |
| 13 | HistoricalMarketCap | Company Info | company | symbol + atDate |
| 14 | CandlestickData | Company Info | market | symbol + timestamp |
| 15 | TechnicalIndicator | Company Info | market | symbol + timestamp + indicator |
| 16 | BasicFinancials | Financials | financials | symbol + metric |
| 17 | CompanyFinancials | Financials | financials | symbol + year + quarter |
| 18 | ReportedFinancials | Financials | financials | symbol + year + quarter |
| 19 | SectorMetrics | Financials | financials | region + sector |
| 20 | EarningsData | Financials | earnings | symbol + period |
| 21 | EarningsCalendar | Financials | earnings | symbol + date |
| 22 | EarningsQualityScore | Financials | financials | symbol + period |
| 23 | Dividend | Financials | trading | symbol + date |
| 24 | AnalystRecommendation | Analyst | analyst | symbol + period |
| 25 | PriceTarget | Analyst | analyst | symbol |
| 26 | UpgradeDowngrade | Analyst | analyst | symbol + gradeTime |
| 27 | RevenueEstimate | Analyst | analyst | symbol + period |
| 28 | EpsEstimate | Analyst | analyst | symbol + period |
| 29 | EbitdaEstimate | Analyst | analyst | symbol + period |
| 30 | EbitEstimate | Analyst | analyst | symbol + period |
| 31 | CompanyOwnership | Ownership | ownership | symbol + investorName |
| 32 | FundOwnership | Ownership | ownership | symbol + name |
| 33 | InstitutionalOwnership | Ownership | ownership | symbol + cik |
| 34 | InstitutionalProfile | Ownership | ownership | cik |
| 35 | InstitutionalPortfolio | Ownership | ownership | cik + symbol |
| 36 | InsiderTransaction | Ownership | ownership | symbol + transactionDate + name |
| 37 | GeneralNews | News | news | id |
| 38 | CompanyNews | News | news | id |
| 39 | PressRelease | News | news | id |
| 40 | IpoCalendar | Trading | trading | symbol + date |
| 41 | StockSplit | Trading | trading | symbol + date |

---

## Usage Examples

### Querying Models

```python
from sqlmodel import select
from finhub_etl.models import CompanyProfile2, RealtimeQuote
from finhub_etl.database.core import get_session

# Query company profile
async for session in get_session():
    statement = select(CompanyProfile2).where(CompanyProfile2.symbol == "AAPL")
    result = await session.execute(statement)
    profile = result.scalar_one_or_none()
    print(profile)

# Query latest quotes
async for session in get_session():
    statement = select(RealtimeQuote).limit(10)
    result = await session.execute(statement)
    quotes = result.scalars().all()
    for quote in quotes:
        print(f"{quote.symbol}: ${quote.c}")
```

### Creating Model Instances

```python
from finhub_etl.models import StockSymbol

# Create a new stock symbol
symbol = StockSymbol(
    symbol="AAPL",
    description="Apple Inc",
    displaySymbol="AAPL",
    type="Common Stock",
    mic="XNAS",
    currency="USD"
)

# Save to database
async for session in get_session():
    session.add(symbol)
    await session.commit()
```

---

## Database Migrations

All models are automatically tracked by Alembic. When you add or modify models:

```bash
# Generate migration
alembic revision --autogenerate -m "Add new model"

# Apply migration
alembic upgrade head

# Check status
alembic current
```

---

## Model Location Reference

- **Models Directory:** `src/finhub_etl/models/`
- **Model Registry:** `src/finhub_etl/models/__init__.py`
- **Handler Mappings:** `src/finhub_etl/utils/mappings.py`
- **Database Core:** `src/finhub_etl/database/core.py`

---

## Related Documentation

- [Handler Configuration](../src/finhub_etl/config/handlers/README.md)
- [Database Setup](../CLAUDE.md#database-architecture)
- [API Mappings](../src/finhub_etl/utils/mappings.py)
- [Finnhub API Documentation](https://finnhub.io/docs/api)

---

**Last Updated:** 2025-11-12
**Total Models:** 41
**Database:** MySQL with async support (aiomysql)
**ORM:** SQLModel 0.0.27
