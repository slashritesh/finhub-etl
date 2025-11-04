# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**finhub-etl** is a Python-based ETL pipeline for extracting financial data from the Finnhub API and loading it into a MySQL database. The project uses SQLModel for ORM, Alembic for migrations, and async SQLAlchemy for database operations.

## Technology Stack

- **Python**: 3.10-3.13
- **ORM**: SQLModel 0.0.27 with async support
- **Database**: MySQL (via aiomysql)
- **Migrations**: Alembic 1.17.1
- **Data Source**: Finnhub API (finnhub-python 2.4.25)
- **Environment**: python-dotenv 0.9.9

## Environment Setup

Two database URLs are required in `.env`:

```
DATABASE_URL=mysql+aiomysql://user:password@host:port/database
SYNC_DATABASE_URL=mysql+pymysql://user:password@host:port/database
FINHUB_API_KEY=your_finnhub_api_key
```

**Critical**:
- `DATABASE_URL` uses async driver (aiomysql) for application code
- `SYNC_DATABASE_URL` uses sync driver (pymysql) for Alembic migrations
- Both must point to the same database

## Running the Application

```bash
# Run the main ETL script
python src/main.py
```

Currently, `src/main.py` fetches Apple (AAPL) annual financial reports and saves them to `data/financials.json`.

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Create empty migration
alembic revision -m "description"
```

### Running Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show history
alembic history
```

### Migration Architecture

- **Models Import**: `migrations/env.py:9-10` imports all models from `src/models/__init__.py`
- **Target Metadata**: `migrations/env.py:36` sets `target_metadata = SQLModel.metadata` for autogenerate
- **Database URL Override**: `migrations/env.py:19-21` loads `SYNC_DATABASE_URL` from environment and overrides alembic.ini

## Project Structure

```
finhub-etl/
├── src/
│   ├── config/         # Configuration (currently empty)
│   ├── database/
│   │   └── core.py     # Async engine and session factory
│   ├── loaders/        # Data loaders (currently empty)
│   ├── models/
│   │   ├── __init__.py # Model registry
│   │   └── company.py  # CompanyProfile model
│   ├── utils/          # Utilities (currently empty)
│   └── main.py         # Finnhub API client & data fetching
├── migrations/
│   ├── env.py          # Alembic configuration with model imports
│   └── versions/       # Migration scripts
├── data/               # Output directory for fetched data
└── scripts/start.sh    # Startup script (currently empty)
```

## Database Architecture

### Async Database Operations

All database operations must use async/await patterns:

```python
from src.database.core import get_session

async def example_operation():
    async with get_session() as session:
        result = await session.execute(query)
        await session.commit()
```

- **Engine**: `src/database/core.py:11` creates async engine from `DATABASE_URL`
- **Session Factory**: `src/database/core.py:14` provides `get_session()` async generator

### Models

Currently only `CompanyProfile` model exists (`src/models/company.py`):
- Maps to Finnhub company profile API response
- Contains 36 fields including address, financial metrics, identifiers (CUSIP, ISIN, SEDOL)
- Uses camelCase field names matching Finnhub API

## Adding New Models

1. Create model in `src/models/` (e.g., `earnings.py`)
2. Import in `src/models/__init__.py` and add to `__all__`
3. Run `alembic revision --autogenerate -m "add earnings model"`
4. Review generated migration in `migrations/versions/`
5. Apply migration: `alembic upgrade head`

**Important**: The migration system is already configured. Models imported in `src/models/__init__.py` are automatically picked up by Alembic's autogenerate via `migrations/env.py:9-10`.

## Finnhub API Integration

The project uses the `finnhub-python` client library. Current implementation in `src/main.py`:
- Initializes client with `FINHUB_API_KEY` from environment
- Fetches financial reports using `financials_reported()` method
- Saves JSON responses to `data/` directory

API key validation occurs at startup - script will fail fast if key is missing.
- When You read file before implementation i am also along with you manually writting fixing code so follow that pattren of code if i am overwitting it