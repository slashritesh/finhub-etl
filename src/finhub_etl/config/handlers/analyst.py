"""Analyst data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, Optional
from finhub_etl.config.finhub import api_client


async def get_recommendation_trends(symbol: str) -> Dict[str, Any]:
    """Get latest analyst recommendation trends for a company.

    Endpoint: /stock/recommendation

    Args:
        symbol: Stock symbol

    Returns:
        Recommendation trends data (buy, hold, sell counts)
    """
    return await api_client.get(
        "/stock/recommendation",
        params={"symbol": symbol}
    )


async def get_price_target(symbol: str) -> Dict[str, Any]:
    """Get latest price target consensus.

    Endpoint: /stock/price-target

    Args:
        symbol: Stock symbol

    Returns:
        Price target data (target high, low, average, median)
    """
    return await api_client.get(
        "/stock/price-target",
        params={"symbol": symbol}
    )


async def get_upgrade_downgrade(
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get latest stock upgrade and downgrade.

    Endpoint: /stock/upgrade-downgrade

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        Upgrade/downgrade data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/stock/upgrade-downgrade", params=params)


async def get_revenue_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> Dict[str, Any]:
    """Get revenue estimates.

    Endpoint: /stock/revenue-estimate

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'quarterly')

    Returns:
        Revenue estimates data
    """
    return await api_client.get(
        "/stock/revenue-estimate",
        params={"symbol": symbol, "freq": freq}
    )


async def get_eps_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> Dict[str, Any]:
    """Get EPS (earnings per share) estimates.

    Endpoint: /stock/eps-estimate

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'quarterly')

    Returns:
        EPS estimates data
    """
    return await api_client.get(
        "/stock/eps-estimate",
        params={"symbol": symbol, "freq": freq}
    )


async def get_ebitda_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> Dict[str, Any]:
    """Get EBITDA estimates.

    Endpoint: /stock/ebitda-estimate

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'quarterly')

    Returns:
        EBITDA estimates data
    """
    return await api_client.get(
        "/stock/ebitda-estimate",
        params={"symbol": symbol, "freq": freq}
    )


async def get_ebit_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> Dict[str, Any]:
    """Get EBIT estimates.

    Endpoint: /stock/ebit-estimate

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'quarterly')

    Returns:
        EBIT estimates data
    """
    return await api_client.get(
        "/stock/ebit-estimate",
        params={"symbol": symbol, "freq": freq}
    )


__all__ = [
    "get_recommendation_trends",
    "get_price_target",
    "get_upgrade_downgrade",
    "get_revenue_estimate",
    "get_eps_estimate",
    "get_ebitda_estimate",
    "get_ebit_estimate",
]
