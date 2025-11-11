"""Market data handlers"""
from ..finhub import api_client


async def get_market_status(exchange: str):
    """Fetch market status for a given exchange.
    Args:
        exchange (str): Exchange code (e.g., 'US', 'UK')
    Returns:
        dict: Market status data
    """
    return await api_client.get("/stock/market-status", params={"exchange": exchange})


async def get_market_holidays(exchange: str):
    """Fetch market holidays for a given exchange.
    Args:
        exchange (str): Exchange code (e.g., 'US', 'UK')
    Returns:
        dict: Market holidays data
    """
    return await api_client.get("/stock/market-holiday", params={"exchange": exchange})


async def get_realtime_quote(symbol: str):
    """Fetch real-time quote for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        dict: Real-time quote data
    """
    return await api_client.get("/quote", params={"symbol": symbol})
