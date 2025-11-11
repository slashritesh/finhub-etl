"""News-related handlers"""
from ..finhub import api_client


async def get_company_news(symbol: str, from_date: str, to_date: str):
    """Fetch company-specific news for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        from_date (str): Start date in YYYY-MM-DD format
        to_date (str): End date in YYYY-MM-DD format
    Returns:
        list: List of news articles
    """
    return await api_client.get(
        "/company-news", params={"symbol": symbol, "from": from_date, "to": to_date}
    )


async def get_general_news(category: str = "general", min_id: int = 0):
    """Fetch general market news.
    Args:
        category (str): News category (general, forex, crypto, merger)
        min_id (int): Minimum news ID for pagination
    Returns:
        list: List of news articles
    """
    return await api_client.get(
        "/news", params={"category": category, "minId": min_id}
    )


async def get_press_release(symbol: str, from_date: str = None, to_date: str = None):
    """Fetch press releases for a given company symbol.
    Args:
        symbol (str): Stock ticker (e.g., 'AAPL')
        from_date (str, optional): Start date 'YYYY-MM-DD'
        to_date (str, optional): End date 'YYYY-MM-DD'
    Returns:
        dict: Press release data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/press-releases2", params=params)
