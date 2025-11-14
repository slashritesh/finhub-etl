# Finhub ETL

A comprehensive ETL (Extract, Transform, Load) pipeline for financial data from the Finnhub API.

## Project Structure

This is a monorepo containing two main services:

```
finhub-etl/
├── etl-pipeline/          # ETL extraction and data ingestion service
│   ├── src/finhub_etl/   # Main ETL application
│   ├── migrations/        # Alembic database migrations
│   └── pyproject.toml     # ETL dependencies
│
└── worker/                # Worker models shared package
    ├── src/worker/       # Worker models and utilities
    └── pyproject.toml    # Worker dependencies
```

## Features

### ETL Pipeline
- **Data Extraction**: Async HTTP client for Finnhub API
- **Scheduled Jobs**: APScheduler for automated data collection
- **Data Models**: 33 SQLModel definitions for financial data
- **Database Migrations**: Alembic-based schema management
- **Handlers**: Organized by domain (analyst, company, earnings, financials, market, news, ownership, trading)

### Data Coverage
- Company profiles and financials
- Analyst recommendations and price targets
- Earnings data and estimates
- Stock quotes and candlestick data
- Ownership information (institutional, fund, company)
- Market news and company news
- Insider transactions and SEC filings
- IPO calendar and stock splits
- Technical indicators and sector metrics

## Prerequisites

- Python >= 3.10
- MySQL database
- Finnhub API key (get one at https://finnhub.io/)
- Poetry (for dependency management)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd finhub-etl
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your database credentials and Finnhub API key
```

### 3. Install dependencies

For ETL Pipeline:
```bash
cd etl-pipeline
poetry install
```

For Worker:
```bash
cd worker
poetry install
```

### 4. Run database migrations
```bash
cd etl-pipeline
poetry run alembic upgrade head
```

### 5. Start the services

Using Docker Compose:
```bash
docker-compose up -d
```

Or manually:
```bash
cd etl-pipeline
poetry run python -m finhub_etl.main
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=mysql+aiomysql://user:password@host:port/database
SYNC_DATABASE_URL=mysql+pymysql://user:password@host:port/database

# Finnhub API
FINHUB_API_KEY=your_api_key_here
```

## Development

### Running Tests
```bash
make test
```

### Code Quality
```bash
make lint
make format
```

### Database Migrations

Create a new migration:
```bash
cd etl-pipeline
poetry run alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
poetry run alembic upgrade head
```

Rollback migrations:
```bash
poetry run alembic downgrade -1
```

## Project Components

### ETL Pipeline Services
- **Scheduler**: APScheduler-based job scheduling
- **Handlers**: API endpoint handlers for different data types
- **Models**: SQLModel database models
- **Loaders**: Data loading utilities
- **Utils**: Helper functions and mappings

### Worker Service
- **Models**: Shared data models for distributed processing

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions, please create an issue in the repository.
