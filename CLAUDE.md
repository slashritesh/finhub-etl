# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based ETL (Extract, Transform, Load) project for financial data called **finhub-etl**. The project uses SQLModel for ORM, Alembic for database migrations, and async SQLAlchemy for database operations.

## Technology Stack

- **Python**: 3.14+
- **ORM**: SQLModel (0.0.27) with async support
- **Database Migrations**: Alembic (1.17.1)
- **Environment Management**: dotenv (0.9.9)
- **Build System**: Poetry Core (2.0.0+)

## Project Structure

```
finhub-etl/
├── src/
│   ├── config/         # Configuration modules
│   ├── database/       # Database setup and session management
│   │   └── core.py     # Async engine and session factory
│   ├── loaders/        # Data loaders (currently empty)
│   ├── models/         # SQLModel database models
│   ├── utils/          # Utility functions
│   └── main.py         # Application entry point
├── migrations/         # Alembic migration files
│   ├── env.py          # Alembic environment configuration
│   ├── versions/       # Migration version scripts
│   └── script.py.mako  # Migration template
├── scripts/            # Shell scripts
│   └── start.sh        # Startup script
├── alembic.ini         # Alembic configuration
└── pyproject.toml      # Project dependencies and metadata
```

## Database Architecture

The project uses an async database architecture:

- **Engine Creation**: `src/database/core.py:11` - Creates async SQLAlchemy engine using DATABASE_URL from environment
- **Session Management**: `src/database/core.py:14` - Async context manager `get_session()` yields AsyncSession instances
- **Environment Variables**: Database URL is loaded from `.env` file via dotenv

### Important Notes on Database

- The project uses **async SQLAlchemy** - all database operations must use `async`/`await`
- Session factory: Use `get_session()` as an async context manager or dependency injector
- Migrations are managed via Alembic in the `migrations/` directory

## Database Migrations

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description of changes"

# Create empty migration
alembic revision -m "description of changes"
```

### Running Migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Migration Configuration

- **Target Metadata**: migrations/env.py:21 - Currently set to `None`, needs to be updated to import models for autogenerate support
- To enable autogenerate, update `migrations/env.py` to import your models and set `target_metadata` to your Base metadata

## Environment Setup

1. **Environment File**: Create/update `.env` in project root with:
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
   ```

2. **Virtual Environment**: Project uses Python 3.14 with a `.venv` directory

3. **Dependencies**: Install via pip:
   ```bash
   pip install -e .
   ```

## Development Workflow

Since most source files are currently empty, the expected workflow is:

1. Define SQLModel models in `src/models/`
2. Update `migrations/env.py` to import models for autogenerate support
3. Create data loaders in `src/loaders/`
4. Implement business logic in `src/main.py`
5. Run migrations to create database schema
6. Execute ETL processes

## Critical Implementation Details

### Adding New Models

When adding new SQLModel models:
1. Create model in `src/models/`
2. Import model in `src/models/__init__.py`
3. Update `migrations/env.py` to import models and set `target_metadata`
4. Generate migration: `alembic revision --autogenerate -m "add model_name"`
5. Review and run migration: `alembic upgrade head`

### Async Database Operations

All database operations must be async. Example pattern:

```python
from src.database.core import get_session

async def example_operation():
    async with get_session() as session:
        # Perform database operations
        result = await session.execute(query)
        await session.commit()
```
