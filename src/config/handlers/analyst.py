"""Analyst data handlers"""
from ..finhub import api_client


async def get_analyst_recommendations(symbol: str):
    """Fetch analyst recommendations for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        list: Analyst recommendations
    """
    return await api_client.get("/stock/recommendation", params={"symbol": symbol})


async def get_price_target(symbol: str):
    """Fetch price target for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        dict: Price target data
    """
    return await api_client.get("/stock/price-target", params={"symbol": symbol})


async def get_upgrade_downgrade(
    symbol: str = None, from_date: str = None, to_date: str = None
):
    """Fetch analyst upgrades/downgrades.
    Args:
        symbol (str, optional): Stock ticker symbol
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Upgrade/downgrade data
    """
    params = {}
    if symbol:
        params["symbol"] = symbol
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/upgrade-downgrade", params=params)
