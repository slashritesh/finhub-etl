"""
Example Handler - Minimal boilerplate for fetching data from APIs

This handler demonstrates:
1. How to make API calls with parameters
2. How to handle optional parameters
3. How to transform API responses for database storage
4. How to handle nested responses
"""

from typing import Optional, List, Dict, Any
import httpx


# Example 1: Simple GET request with required params
async def fetch_simple_data(symbol: str, endpoint: str = "https://api.example.com/data") -> Dict[str, Any]:
    """
    Fetch data from an API endpoint with basic parameters.

    Args:
        symbol: Stock symbol (e.g., "AAPL")
        endpoint: API endpoint URL

    Returns:
        Dictionary with the API response
    """
    params = {"symbol": symbol}

    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()


# Example 2: GET request with optional parameters
async def fetch_data_with_options(
    symbol: str,
    data_type: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    endpoint: str = "https://api.example.com/advanced"
) -> Dict[str, Any]:
    """
    Fetch data with optional parameters (filters out None values).

    Args:
        symbol: Stock symbol (required)
        data_type: Type of data to fetch (required)
        from_date: Start date (optional, format: YYYY-MM-DD)
        to_date: End date (optional, format: YYYY-MM-DD)
        endpoint: API endpoint URL

    Returns:
        Dictionary with the API response
    """
    # Build params dictionary
    all_params = {
        "symbol": symbol,
        "type": data_type,
        "from": from_date,
        "to": to_date,
    }

    # Filter out None values
    active_params = {key: value for key, value in all_params.items() if value is not None}

    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, params=active_params, timeout=30.0)
        response.raise_for_status()
        return response.json()


# Example 3: Transform nested API response to flat structure
async def fetch_and_flatten(
    symbol: str,
    endpoint: str = "https://api.example.com/nested"
) -> List[Dict[str, Any]]:
    """
    Fetch nested data and flatten it for database storage.

    API might return:
    {
        "symbol": "AAPL",
        "items": [
            {"value": 100, "date": "2024-01-01"},
            {"value": 105, "date": "2024-01-02"}
        ]
    }

    We transform it to:
    [
        {"symbol": "AAPL", "value": 100, "date": "2024-01-01"},
        {"symbol": "AAPL", "value": 105, "date": "2024-01-02"}
    ]
    """
    # Fetch data
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, params={"symbol": symbol}, timeout=30.0)
        response.raise_for_status()
        raw_data = response.json()

    # Handle empty response
    if not raw_data or "items" not in raw_data:
        return []

    # Flatten the structure
    flattened = []
    for item in raw_data["items"]:
        flattened.append({
            "symbol": symbol,  # Add parent info to each item
            "value": item.get("value"),
            "data_date": item.get("date"),  # Rename field
        })

    return flattened


# Example 4: Using your existing Finnhub client pattern
# Uncomment and modify if you want to use the existing api_client
"""
from worker.config.finhub import api_client

async def fetch_using_finhub_client(symbol: str) -> Dict[str, Any]:
    '''
    Use the existing Finnhub API client.
    '''
    params = {"symbol": symbol}
    return await api_client.get("/your/endpoint", params=params)
"""


__all__ = [
    "fetch_simple_data",
    "fetch_data_with_options",
    "fetch_and_flatten",
]
