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
) -> Dict[str, Any]:
    """Get earnings calendar for specified date range.

    Endpoint: /calendar/earnings

    Args:
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        symbol: Filter by symbol (optional)
        international: Include international markets (default: False)

    Returns:
        Earnings calendar data
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
    return await api_client.get("/calendar/earnings", params=params)


__all__ = [
    "get_earnings",
    "get_earnings_calendar",
]
