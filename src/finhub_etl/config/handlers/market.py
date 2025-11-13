"""Market data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, Optional, List
from finhub_etl.config.finhub import api_client
from finhub_etl.models.market_info import MarketHoliday


async def get_symbol_lookup(query: str) -> Dict[str, Any]:
    """Search for best-matching symbols and market information.

    Endpoint: /search

    Args:
        query: Search query (company name or symbol)

    Returns:
        Matching symbols data with description and type
    """
    return await api_client.get("/search", params={"q": query})


async def get_stock_symbols(
    exchange: str,
    mic: Optional[str] = None,
    security_type: Optional[str] = None,
    currency: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get list of supported stocks for an exchange.

    Endpoint: /stock/symbol

    Args:
        exchange: Exchange code (e.g., 'US')
        mic: Market Identifier Code (optional)
        security_type: Security type filter (optional)
        currency: Currency filter (optional)

    Returns:
        List of stock symbols with metadata
    """
    params = {"exchange": exchange}
    if mic:
        params["mic"] = mic
    if security_type:
        params["securityType"] = security_type
    if currency:
        params["currency"] = currency
    return await api_client.get("/stock/symbol", params=params)


async def get_market_status(exchange: str) -> Dict[str, Any]:
    """Get current market status (open/closed).

    Endpoint: /stock/market-status

    Args:
        exchange: Exchange code (e.g., 'US')

    Returns:
        Market status data (isOpen, session, timezone, etc.)
    """
    return await api_client.get(
        "/stock/market-status",
        params={"exchange": exchange}
    )


async def get_market_holiday(exchange: str) -> List[Dict[str, Any]]:
    """
    Fetch and transform market holiday data for a given exchange.

    Endpoint: /stock/market-holiday

    Args:
        exchange: Exchange code (e.g., 'US')

    Returns:
        List[Dict[str, Any]] records (JSON ready for DB insertion)
    """
    response: Dict[str, Any] = await api_client.get(
        "/stock/market-holiday",
        params={"exchange": exchange}
    )

    if not response or "data" not in response:
        return []

    # Transform API data into JSON objects
    records = [
        {
            "exchange": response.get("exchange", exchange),
            "timezone": response.get("timezone", ""),
            "date": item.get("atDate"),
            "event_name": item.get("eventName"),
            "trading_hour": item.get("tradingHour", "")
        }
        for item in response["data"]
    ]

    return records

async def get_quote(symbol: str) -> Dict[str, Any]:
    """Get real-time quote data for US stocks.

    Endpoint: /quote

    Args:
        symbol: Stock symbol

    Returns:
        Real-time quote (current, high, low, open, previous close, change, percent change)
    """
    data = await api_client.get("/quote", params={"symbol": symbol})
    data["symbol"] = symbol
    return data


async def get_candles(
    symbol: str,
    resolution: str,
    from_timestamp: int,
    to_timestamp: int
) -> Dict[str, Any]:
    """Get candlestick data (OHLCV) for stocks.

    Endpoint: /stock/candle

    Args:
        symbol: Stock symbol
        resolution: Candle resolution (1, 5, 15, 30, 60, D, W, M)
        from_timestamp: UNIX timestamp in seconds
        to_timestamp: UNIX timestamp in seconds

    Returns:
        OHLCV data arrays (open, high, low, close, volume, timestamp)
    """
    data = await api_client.get(
        "/stock/candle",
        params={
            "symbol": symbol,
            "resolution": resolution,
            "from": from_timestamp,
            "to": to_timestamp
        }
    )
    data["symbol"] = symbol
    return data


async def get_technical_indicators(
    symbol: str,
    resolution: str,
    from_timestamp: int,
    to_timestamp: int,
    indicator: str,
    **indicator_fields
) -> Dict[str, Any]:
    """Get technical indicator values.

    Endpoint: /indicator

    Args:
        symbol: Stock symbol
        resolution: Candle resolution (1, 5, 15, 30, 60, D, W, M)
        from_timestamp: UNIX timestamp in seconds
        to_timestamp: UNIX timestamp in seconds
        indicator: Indicator name (e.g., 'rsi', 'macd', 'ema', 'sma', etc.)
        **indicator_fields: Additional indicator parameters (e.g., timeperiod=14)

    Returns:
        Technical indicator data

    Example:
        >>> # Get RSI with 14-day period
        >>> await get_technical_indicators(
        ...     "AAPL", "D", 1590988249, 1591852249, "rsi", timeperiod=14
        ... )
    """
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": from_timestamp,
        "to": to_timestamp,
        "indicator": indicator,
        **indicator_fields
    }
    return await api_client.get("/indicator", params=params)


__all__ = [
    "get_symbol_lookup",
    "get_stock_symbols",
    "get_market_status",
    "get_market_holiday",
    "get_quote",
    "get_candles",
    "get_technical_indicators",
]
