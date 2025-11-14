"""News data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, Optional, List
from worker.config.finhub import api_client


async def get_general_news(
    category: str,
    min_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Get general market news.

    Endpoint: /news

    Args:
        category: News category ('general', 'forex', 'crypto', 'merger')
        min_id: Minimum news ID for pagination (optional)

    Returns:
        List of news articles
    """
    params = {"category": category}
    if min_id:
        params["minId"] = min_id
    return await api_client.get("/news", params=params)


async def get_company_news(
    symbol: str,
    from_date: str,
    to_date: str
) -> List[Dict[str, Any]]:
    """Get company-specific news.

    Endpoint: /company-news

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        List of company news articles
    """
    data =  await api_client.get(
        "/company-news",
        params={"symbol": symbol, "from": from_date, "to": to_date}
    )

    # Inject symbol into each news object
    for item in data:
        item["symbol"] = symbol

    return data


async def get_press_releases(
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get company press releases.

    Endpoint: /press-releases2

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD, optional)
        to_date: End date (YYYY-MM-DD, optional)

    Returns:
        List of press releases with converted date + symbol added
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    data = await api_client.get("/press-releases2", params=params)
    items = data.get("pressReleases", [])

    for item in items:
        # Ensure symbol exists
        item["symbol"] = symbol
        item["date"] = item.pop("datetime")
    return items



__all__ = [
    "get_general_news",
    "get_company_news",
    "get_press_releases",
]
