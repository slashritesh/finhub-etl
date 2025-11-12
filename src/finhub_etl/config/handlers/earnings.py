"""Earnings data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, Optional, List
from finhub_etl.config.finhub import api_client


async def get_earnings(
    symbol: str,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get historical quarterly earnings surprise data.

    Endpoint: /stock/earnings

    Args:
        symbol: Stock symbol
        limit: Number of results to return

    Returns:
        List of earnings surprise data
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    return await api_client.get("/stock/earnings", params=params)


async def get_earnings_calendar(
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    symbol: Optional[str] = None,
    international: Optional[bool] = False
) -> List[Dict[str, Any]]:  # <-- The return type is now a List
    """
    Get earnings calendar and formats the response for storage.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if symbol:
        params["symbol"] = symbol
    if international:
        params["international"] = international
        
    # 1. Fetch the raw, nested response
    raw_response = await api_client.get("/calendar/earnings", params=params)

    # 2. Handle empty or malformed responses
    if not raw_response or "earningsCalendar" not in raw_response:
        return []

    # 3. Extract and return the clean list of earnings data.
    #    No other processing is needed as the symbol is already in each record.
    return raw_response["earningsCalendar"]


__all__ = [
    "get_earnings",
    "get_earnings_calendar",
]
