# ETL Utilities Usage Guide

This guide explains how to use the reusable ETL utilities for fetching data from Finnhub API and storing it in the database.

## Overview

The ETL utilities provide a flexible, mapping-based approach to fetch data from Finnhub API handlers and automatically store them in the database using SQLModel.

## Core Components

### 1. `fetch_and_store()`

Single operation to fetch data and store in database.

```python
from src.config import get_company_profile
from src.models.company import CompanyProfile
from src.utils import fetch_and_store

result = await fetch_and_store(
    handler_func=get_company_profile,
    model_class=CompanyProfile,
    handler_params={'symbol': 'AAPL'}
)
```

**Parameters:**
- `handler_func`: Finnhub API handler function
- `model_class`: SQLModel class to instantiate
- `handler_params`: Dictionary of parameters for the handler
- `transform_func`: Optional function to transform API response
- `extra_fields`: Optional dictionary of extra fields to add

### 2. `batch_fetch_and_store()`

Execute multiple fetch-and-store operations.

```python
from src.utils import batch_fetch_and_store, get_company_data_mappings

mappings = get_company_data_mappings('AAPL')
results = await batch_fetch_and_store(mappings)
```

**Returns:** Dictionary with results for each operation including success status and record count.

### 3. Mapping Functions

Pre-configured mapping generators for common data fetching patterns:

- `get_company_data_mappings(symbol)` - Company profile, quote, peers, financials
- `get_news_mappings(symbol, days_back)` - Company news
- `get_market_data_mappings(symbol, resolution, days_back)` - Stock candles
- `get_estimates_mappings(symbol, freq)` - Revenue and EPS estimates
- `get_analyst_data_mappings(symbol)` - Analyst recommendations
- `get_corporate_actions_mappings(symbol, days_back)` - Dividends, splits
- `get_ownership_mappings(symbol, days_back)` - Insider transactions
- `get_full_company_mappings(symbol)` - All available data

### 4. Transform Functions

Helper functions to transform API responses:

- `transform_candles_response(data, symbol, resolution)` - Convert candle arrays to records
- `transform_peers_response(data, symbol)` - Convert peer array to relationships
- `transform_estimates_response(data)` - Extract estimates data array
- `transform_news_response(data)` - Pass-through for news data

## Usage Patterns

### Pattern 1: Fetch Single Data Point

```python
from src.config import get_quote
from src.models.market_data import StockQuote
from src.utils import fetch_and_store

quote = await fetch_and_store(
    handler_func=get_quote,
    model_class=StockQuote,
    handler_params={'symbol': 'AAPL'},
    extra_fields={'symbol': 'AAPL'}
)
```

### Pattern 2: Fetch with Transformation

```python
from src.config import get_peers
from src.models.company_data import CompanyPeer
from src.utils import fetch_and_store, transform_peers_response

symbol = 'AAPL'
peers = await fetch_and_store(
    handler_func=get_peers,
    model_class=CompanyPeer,
    handler_params={'symbol': symbol},
    transform_func=lambda data: transform_peers_response(data, symbol)
)
```

### Pattern 3: Batch Operations with Pre-configured Mappings

```python
from src.utils import batch_fetch_and_store, get_company_data_mappings

# Fetch all company data
mappings = get_company_data_mappings('MSFT')
results = await batch_fetch_and_store(mappings)

# Check results
for name, result in results.items():
    if result['success']:
        print(f"{name}: {result['count']} records saved")
```

### Pattern 4: Custom Mapping

```python
from src.config import get_company_news
from src.models.news import CompanyNews
from src.utils import batch_fetch_and_store

mappings = [
    {
        'name': 'aapl_news',
        'handler_func': get_company_news,
        'model_class': CompanyNews,
        'handler_params': {
            'symbol': 'AAPL',
            'from_date': '2024-01-01',
            'to_date': '2024-12-31'
        },
        'extra_fields': {'symbol': 'AAPL'}
    }
]

results = await batch_fetch_and_store(mappings)
```

### Pattern 5: Multiple Symbols

```python
from src.utils import batch_fetch_and_store, get_company_data_mappings

symbols = ['AAPL', 'GOOGL', 'MSFT']

all_mappings = []
for symbol in symbols:
    all_mappings.extend(get_company_data_mappings(symbol))

results = await batch_fetch_and_store(all_mappings)
```

## Mapping Dictionary Structure

A mapping dictionary contains:

```python
{
    'name': 'operation_name',              # Identifier for logging
    'handler_func': handler_function,      # Function to call
    'model_class': ModelClass,             # SQLModel class
    'handler_params': {'key': 'value'},    # Handler parameters
    'transform_func': transform_func,      # Optional: Transform response
    'extra_fields': {'key': 'value'}       # Optional: Add extra fields
}
```

## Examples

See `examples/etl_usage.py` for complete working examples including:

1. Single data fetch
2. Data transformation
3. Batch operations
4. Market data (candles)
5. News data
6. Full company dataset
7. Multiple symbols

Run examples:

```bash
python examples/etl_usage.py
```

## Error Handling

The utilities include automatic error handling:

- Failed operations return `None` or empty results
- Errors are logged with details
- Batch operations continue even if individual operations fail
- Results include success status for each operation

## Best Practices

1. **Use pre-configured mappings** when possible for consistency
2. **Add logging** to track data fetching progress
3. **Handle rate limits** by spacing out API calls
4. **Use batch operations** for efficiency
5. **Transform data** when API response doesn't match model structure
6. **Add extra fields** (like symbol) to enable proper database queries

## Advanced Usage

### Custom Transform Function

```python
def custom_transform(data):
    """Transform API response to match model."""
    if not data:
        return []

    # Your transformation logic
    transformed = []
    for item in data:
        transformed.append({
            'field1': item['apiField1'],
            'field2': item['apiField2'],
            # ... more mappings
        })

    return transformed

result = await fetch_and_store(
    handler_func=my_handler,
    model_class=MyModel,
    handler_params={'param': 'value'},
    transform_func=custom_transform
)
```

### Dynamic Mappings

```python
def get_dynamic_mappings(symbols, date_range):
    """Generate mappings dynamically."""
    mappings = []

    for symbol in symbols:
        for category in ['news', 'candles', 'estimates']:
            mappings.append({
                'name': f'{symbol}_{category}',
                # ... configuration
            })

    return mappings
```

## Troubleshooting

**Issue:** Data not saving to database
- Check database connection
- Verify model field names match API response
- Check for validation errors in logs

**Issue:** Transform function errors
- Verify API response structure matches expectations
- Add defensive checks for missing fields
- Use optional fields in models

**Issue:** Rate limit errors
- Add delays between API calls
- Use smaller batches
- Check your Finnhub API plan limits
