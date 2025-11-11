"""Trading data handlers"""
from ..finhub import api_client


async def get_candlestick_data(
    symbol: str, resolution: str, from_ts: int, to_ts: int
):
    """Fetch historical candlestick data.
    Args:
        symbol (str): Stock ticker symbol
        resolution (str): Resolution (1, 5, 15, 30, 60, D, W, M)
        from_ts (int): From timestamp (Unix)
        to_ts (int): To timestamp (Unix)
    Returns:
        dict: Candlestick data
    """
    return await api_client.get(
        "/stock/candle",
        params={
            "symbol": symbol,
            "resolution": resolution,
            "from": from_ts,
            "to": to_ts,
        },
    )


async def get_stock_splits(symbol: str, from_date: str, to_date: str):
    """Fetch stock split data.
    Args:
        symbol (str): Stock ticker symbol
        from_date (str): Start date in YYYY-MM-DD format
        to_date (str): End date in YYYY-MM-DD format
    Returns:
        list: Stock split data
    """
    return await api_client.get(
        "/stock/split", params={"symbol": symbol, "from": from_date, "to": to_date}
    )


async def get_technical_indicators(
    symbol: str, resolution: str, from_ts: int, to_ts: int, indicator: str, **kwargs
):
    """Fetch technical indicators.
    Args:
        symbol (str): Stock ticker symbol
        resolution (str): Resolution (1, 5, 15, 30, 60, D, W, M)
        from_ts (int): From timestamp (Unix)
        to_ts (int): To timestamp (Unix)
        indicator (str): Indicator name (rsi, macd, sma, ema, etc.)
        **kwargs: Additional indicator-specific parameters
    Returns:
        dict: Technical indicator data
    """
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": from_ts,
        "to": to_ts,
        "indicator": indicator,
    }
    params.update(kwargs)

    return await api_client.get("/indicator", params=params)
