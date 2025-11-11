"""
ETL utility functions for fetching data from Finnhub API and storing in database.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union
from sqlmodel import SQLModel

from database.core import get_session

T = TypeVar("T", bound=SQLModel)

logger = logging.getLogger(__name__)


async def fetch_and_store(
    handler_func: Callable,
    model_class: Type[T],
    handler_params: Dict[str, Any],
    transform_func: Optional[Callable[[Any], Union[Dict, List[Dict]]]] = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> Union[T, List[T], None]:
    """
    Fetch data from Finnhub API handler and store in database.

    Args:
        handler_func: Finnhub API handler function to call
        model_class: SQLModel class to instantiate
        handler_params: Parameters to pass to handler function
        transform_func: Optional function to transform API response before saving
        extra_fields: Optional extra fields to add to each record (e.g., symbol)

    Returns:
        Created model instance(s) or None if error

    Example:
        from src.config import get_company_profile
        from src.models.company import CompanyProfile

        company = await fetch_and_store(
            handler_func=get_company_profile,
            model_class=CompanyProfile,
            handler_params={'symbol': 'AAPL'}
        )
    """
    try:
        # Fetch data from API
        logger.info(f"Fetching data using {handler_func.__name__} with params: {handler_params}")
        data = handler_func(**handler_params)

        if not data:
            logger.warning(f"No data returned from {handler_func.__name__}")
            return None

        # Transform data if transform function provided
        if transform_func:
            data = transform_func(data)

        # Add extra fields if provided
        if extra_fields:
            if isinstance(data, list):
                for item in data:
                    item.update(extra_fields)
            else:
                data.update(extra_fields)

        # Save to database
        logger.info(f"Saving data to {model_class.__tablename__}")
        result = await save_to_db(model_class, data)

        logger.info(f"Successfully saved {len(result) if isinstance(result, list) else 1} record(s)")
        return result

    except Exception as e:
        logger.error(f"Error in fetch_and_store: {str(e)}", exc_info=True)
        return None


async def batch_fetch_and_store(
    mappings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Execute multiple fetch and store operations based on mapping configuration.

    Args:
        mappings: List of mapping dictionaries with keys:
            - handler_func: Handler function to call
            - model_class: SQLModel class
            - handler_params: Parameters for handler
            - transform_func: Optional transform function
            - extra_fields: Optional extra fields
            - name: Optional name for logging

    Returns:
        Dictionary with results for each mapping

    Example:
        from src.config import get_company_profile, get_company_news
        from src.models.company import CompanyProfile
        from src.models.news import CompanyNews

        mappings = [
            {
                'name': 'company_profile',
                'handler_func': get_company_profile,
                'model_class': CompanyProfile,
                'handler_params': {'symbol': 'AAPL'}
            },
            {
                'name': 'company_news',
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
    """
    results = {}

    for idx, mapping in enumerate(mappings):
        name = mapping.get('name', f"mapping_{idx}")
        logger.info(f"Processing mapping: {name}")

        result = await fetch_and_store(
            handler_func=mapping['handler_func'],
            model_class=mapping['model_class'],
            handler_params=mapping['handler_params'],
            transform_func=mapping.get('transform_func'),
            extra_fields=mapping.get('extra_fields'),
        )

        results[name] = {
            'success': result is not None,
            'data': result,
            'count': len(result) if isinstance(result, list) else (1 if result else 0)
        }

    return results


async def save_to_db(
    model_class: Type[T],
    data: Union[Dict, List[Dict]],
) -> Union[T, List[T], None]:
    """
    Save data to database using SQLModel.

    Args:
        model_class: SQLModel class to instantiate
        data: Dictionary or list of dictionaries to save

    Returns:
        Created model instance(s) or None if error

    Example:
        from src.models.company import CompanyProfile
        company = await save_to_db(CompanyProfile, company_data)
    """
    try:
        async with get_session() as session:
            if isinstance(data, list):
                if not data:
                    return []

                instances = [model_class(**item) for item in data]
                session.add_all(instances)
                await session.commit()

                for instance in instances:
                    await session.refresh(instance)

                return instances
            else:
                instance = model_class(**data)
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
                return instance

    except Exception as e:
        logger.error(f"Error saving to database: {str(e)}", exc_info=True)
        return None


def transform_news_response(data: List[Dict]) -> List[Dict]:
    """
    Transform news API response to match model structure.

    Args:
        data: List of news items from API

    Returns:
        Transformed list ready for database insertion
    """
    if not isinstance(data, list):
        return []

    return data


def transform_candles_response(data: Dict, symbol: str, resolution: str) -> List[Dict]:
    """
    Transform candles API response to individual records.

    The API returns arrays for t, o, h, l, c, v.
    This function transforms them into individual candle records.

    Args:
        data: Candles response from API with arrays
        symbol: Stock symbol
        resolution: Candle resolution

    Returns:
        List of candle dictionaries

    Example:
        response = {'t': [1234, 5678], 'o': [100, 101], ...}
        candles = transform_candles_response(response, 'AAPL', 'D')
    """
    if data.get('s') != 'ok':
        return []

    timestamps = data.get('t', [])
    opens = data.get('o', [])
    highs = data.get('h', [])
    lows = data.get('l', [])
    closes = data.get('c', [])
    volumes = data.get('v', [])

    candles = []
    for i in range(len(timestamps)):
        candles.append({
            'symbol': symbol,
            'resolution': resolution,
            't': timestamps[i],
            'o': opens[i],
            'h': highs[i],
            'l': lows[i],
            'c': closes[i],
            'v': volumes[i] if i < len(volumes) else None,
            's': data.get('s')
        })

    return candles


def transform_peers_response(data: List[str], symbol: str) -> List[Dict]:
    """
    Transform peers API response to records.

    API returns array of peer symbols.
    This transforms them into relationship records.

    Args:
        data: List of peer symbols
        symbol: Primary stock symbol

    Returns:
        List of peer relationship dictionaries
    """
    if not isinstance(data, list):
        return []

    return [{'symbol': symbol, 'peer': peer} for peer in data]


def transform_estimates_response(data: Dict) -> List[Dict]:
    """
    Transform estimates API response to records.

    API returns nested structure with 'data' array.

    Args:
        data: Estimates response from API

    Returns:
        List of estimate dictionaries
    """
    if not isinstance(data, dict):
        return []

    return data.get('data', [])
