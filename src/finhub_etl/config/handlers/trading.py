"""Trading-related data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, List
from finhub_etl.config.finhub import api_client


async def get_ipo_calendar(
    from_date: str,
    to_date: str
) -> Dict[str, Any]:
    """Get IPO calendar for specified date range.

    Endpoint: /calendar/ipo

    Args:
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        IPO calendar data with upcoming and recent IPOs
    """
    return await api_client.get(
        "/calendar/ipo",
        params={"from": from_date, "to": to_date}
    )


async def get_dividends(
    symbol: str,
    from_date: str,
    to_date: str
) -> List[Dict[str, Any]]:
    """Get dividend data for a stock.

    Endpoint: /stock/dividend

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        List of dividend events with amount, ex-date, payment date, etc.
    """
    return await api_client.get(
        "/stock/dividend",
        params={"symbol": symbol, "from": from_date, "to": to_date}
    )


async def get_splits(
    symbol: str,
    from_date: str,
    to_date: str
) -> List[Dict[str, Any]]:
    """Get stock split data.

    Endpoint: /stock/split

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        List of stock split events with split ratio and dates
    """
    return await api_client.get(
        "/stock/split",
        params={"symbol": symbol, "from": from_date, "to": to_date}
    )


__all__ = [
    "get_ipo_calendar",
    "get_dividends",
    "get_splits",
]
