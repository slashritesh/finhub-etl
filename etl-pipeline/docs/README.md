# Finhub ETL Documentation

Welcome to the finhub-etl project documentation. This directory contains comprehensive guides and references for working with the Finnhub API ETL pipeline.

## 📚 Documentation Index

### Core Documentation

- **[MODELS.md](./MODELS.md)** - Complete database models reference
  - 41 SQLModel classes
  - Field descriptions and relationships
  - Usage examples and migration guides

### Project Documentation

- **[CLAUDE.md](../CLAUDE.md)** - Project overview and setup guide
  - Technology stack
  - Environment setup
  - Database migrations
  - Running the application

## 🗂️ Project Structure

```
finhub-etl/
├── docs/                          # Documentation (you are here)
│   ├── README.md                  # This file
│   └── MODELS.md                  # Database models reference
│
├── src/finhub_etl/                # Main application package
│   ├── config/
│   │   └── handlers/              # API handler functions (41 handlers)
│   │       ├── analyst.py         # Analyst coverage handlers (7)
│   │       ├── company.py         # Company info handlers (8)
│   │       ├── earnings.py        # Earnings handlers (2)
│   │       ├── financials.py      # Financial statements handlers (5)
│   │       ├── market.py          # Market data handlers (7)
│   │       ├── news.py            # News handlers (3)
│   │       ├── ownership.py       # Ownership handlers (6)
│   │       └── trading.py         # Trading events handlers (3)
│   │
│   ├── database/
│   │   └── core.py                # Async database engine and session
│   │
│   ├── models/                    # SQLModel classes (41 models)
│   │   ├── __init__.py            # Model registry
│   │   ├── analyst.py             # Analyst models (3)
│   │   ├── candle.py              # Candlestick data
│   │   ├── company_news.py        # Company news
│   │   ├── company_peers.py       # Company peers
│   │   ├── company_profile.py     # Company profiles (2)
│   │   ├── dividend.py            # Dividend data
│   │   ├── earnings.py            # Earnings models (2)
│   │   ├── earnings_quality.py    # Earnings quality
│   │   ├── employee_count.py      # Employee count
│   │   ├── estimates.py           # Estimate models (4)
│   │   ├── executive.py           # Executive data
│   │   ├── filing.py              # SEC filings
│   │   ├── financials.py          # Financial statements (3)
│   │   ├── general_news.py        # General news
│   │   ├── historical_mcap.py     # Historical market cap
│   │   ├── institutional.py       # Institutional data (2)
│   │   ├── insider_transaction.py # Insider transactions
│   │   ├── ipo_calendar.py        # IPO calendar
│   │   ├── market_info.py         # Market status/holiday (2)
│   │   ├── matched_stock.py       # Symbol search results
│   │   ├── ownership.py           # Ownership models (3)
│   │   ├── press_release.py       # Press releases
│   │   ├── price_metrics.py       # Price metrics
│   │   ├── quote.py               # Real-time quotes
│   │   ├── sector_metrics.py      # Sector metrics
│   │   ├── stock_split.py         # Stock splits
│   │   ├── symbols.py             # Stock symbols
│   │   └── technical_indicator.py # Technical indicators
│   │
│   ├── utils/
│   │   └── mappings.py            # Handler-Model-Endpoint mappings
│   │
│   └── main.py                    # Application entry point
│
├── tests/                         # Test scripts
│   ├── test_model_handler.py      # Handler testing
│   └── test_store_db.py           # Database storage testing
│
├── migrations/                    # Alembic migrations
│   ├── env.py                     # Migration environment
│   └── versions/                  # Migration scripts
│
├── data/                          # Output directory
├── .env                           # Environment variables
├── alembic.ini                    # Alembic configuration
└── pyproject.toml                 # Poetry dependencies
```

## 📊 Quick Stats

- **Total Models:** 41
- **Total Handlers:** 41
- **API Endpoints:** 41
- **Handler Modules:** 8 categories
- **Database:** MySQL with async support
- **ORM:** SQLModel 0.0.27
- **Migration Tool:** Alembic 1.17.1

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
poetry install

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 2. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current
```

### 3. Test Handlers

```bash
# Test single handler
python tests/test_model_handler.py

# Test database storage
python tests/test_store_db.py
```

## 📖 Key Concepts

### Handler-Model-Endpoint Mapping

Every API endpoint has a corresponding:
1. **Handler function** - Fetches data from Finnhub API
2. **SQLModel class** - Stores data in MySQL
3. **Endpoint URL** - Finnhub API endpoint
4. **Parameters** - Required/optional parameters

Example mapping:
```python
"company_profile2": {
    "handler": company.get_company_profile2,
    "model": CompanyProfile2,
    "endpoint": "/stock/profile2",
    "params": {
        "symbol": "AAPL"
    }
}
```

### Model Categories

1. **Market Data** (5 models) - Symbols, quotes, market status
2. **Company Information** (10 models) - Profiles, executives, filings
3. **Financial Statements** (8 models) - Financials, earnings, dividends
4. **Analyst Coverage** (7 models) - Recommendations, estimates, targets
5. **Ownership Data** (5 models) - Institutional, fund, insider holdings
6. **News & Press** (3 models) - News articles, press releases
7. **Trading Events** (3 models) - IPOs, splits, dividends

### Database Operations

All database operations are async:

```python
from finhub_etl.database.core import get_session
from finhub_etl.models import CompanyProfile2

async for session in get_session():
    # Query
    result = await session.execute(select(CompanyProfile2))

    # Insert
    session.add(model_instance)
    await session.commit()
```

## 🧪 Testing

### Test Handler Only
```python
# tests/test_model_handler.py
TEST_KEY = "company_profile2"  # Change handler key
python tests/test_model_handler.py
```

### Test Handler + Database Storage
```python
# tests/test_store_db.py
TEST_KEY = "company_profile2"  # Change handler key
python tests/test_store_db.py
```

### Test Multiple Handlers
```python
# tests/test_store_db.py
# Uncomment the last line:
asyncio.run(test_multiple_handlers())
```

## 🔧 Configuration Files

### Environment Variables (.env)
```bash
DATABASE_URL=mysql+aiomysql://user:pass@host:port/database
SYNC_DATABASE_URL=mysql+pymysql://user:pass@host:port/database
FINHUB_API_KEY=your_api_key
```

### Handler Mappings (src/finhub_etl/utils/mappings.py)
- Maps handlers to models and endpoints
- Defines default parameters
- Single source of truth for all mappings

## 📝 Adding New Models

1. Create model file in `src/finhub_etl/models/`
2. Import in `src/finhub_etl/models/__init__.py`
3. Create handler in `src/finhub_etl/config/handlers/`
4. Add mapping in `src/finhub_etl/utils/mappings.py`
5. Generate migration: `alembic revision --autogenerate -m "description"`
6. Apply migration: `alembic upgrade head`

## 🔗 External Links

- [Finnhub API Documentation](https://finnhub.io/docs/api)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

## 📞 Support

For issues and questions:
- Check [MODELS.md](./MODELS.md) for model-specific documentation
- Review [CLAUDE.md](../CLAUDE.md) for setup and configuration
- Examine handler code in `src/finhub_etl/config/handlers/`
- Review model definitions in `src/finhub_etl/models/`

---

**Project:** finhub-etl
**Version:** 1.0.0
**Python:** 3.10-3.13
**Database:** MySQL
**API:** Finnhub.io
**Last Updated:** 2025-11-12
