"""Earnings-related handlers"""
from ..finhub import api_client


async def get_earnings_data(symbol: str, limit: int = None):
    """Fetch earnings data for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        limit (int, optional): Number of records to return
    Returns:
        list: Earnings data
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit

    return await api_client.get("/stock/earnings", params=params)


async def get_earnings_calendar(
    from_date: str = None,
    to_date: str = None,
    symbol: str = None,
    international: bool = False,
):
    """Fetch earnings calendar.
    Args:
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
        symbol (str, optional): Filter by symbol
        international (bool): Include international companies
    Returns:
        dict: Earnings calendar data
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if symbol:
        params["symbol"] = symbol
    if international:
        params["international"] = "true"

    return await api_client.get("/calendar/earnings", params=params)


async def get_earnings_quality_score(symbol: str, freq: str = "annual"):
    """Fetch earnings quality score for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: Earnings quality score data
    """
    return await api_client.get(
        "/stock/earnings-quality-score", params={"symbol": symbol, "freq": freq}
    )
