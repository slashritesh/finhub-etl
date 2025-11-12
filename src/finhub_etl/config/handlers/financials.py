"""Financial data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, Optional
from finhub_etl.config.finhub import api_client


async def get_basic_financials(
    symbol: str,
    metric: Optional[str] = "all"
) -> Dict[str, Any]:
    """Get company basic financials such as margin, P/E ratio, 52-week high/low etc.

    Endpoint: /stock/metric

    Args:
        symbol: Stock symbol
        metric: Metric type or 'all' (default: 'all')

    Returns:
        Basic financial metrics
    """
    return await api_client.get(
        "/stock/metric",
        params={"symbol": symbol, "metric": metric}
    )


async def get_financials(
    symbol: str,
    statement: str,
    freq: Optional[str] = "annual"
) -> Dict[str, Any]:
    """Get standardized balance sheet, income statement and cash flow.

    Endpoint: /stock/financials

    Args:
        symbol: Stock symbol
        statement: Statement type ('bs' for balance sheet, 'ic' for income statement, 'cf' for cash flow)
        freq: Frequency - 'annual' or 'quarterly' (default: 'annual')

    Returns:
        Standardized financial statements
    """
    return await api_client.get(
        "/stock/financials",
        params={"symbol": symbol, "statement": statement, "freq": freq}
    )


async def get_financials_reported(
    symbol: str,
    freq: Optional[str] = "annual"
) -> Dict[str, Any]:
    """Get financial statements as reported (not standardized).

    Endpoint: /stock/financials-reported

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'annual')

    Returns:
        As-reported financial statements
    """
    return await api_client.get(
        "/stock/financials-reported",
        params={"symbol": symbol, "freq": freq}
    )


async def get_sector_metrics(region: str) -> Dict[str, Any]:
    """Get sector metrics including performance, valuation, and financial ratios.

    Endpoint: /sector/metrics

    Args:
        region: Region code (e.g., 'us')

    Returns:
        Sector performance metrics
    """
    return await api_client.get(
        "/sector/metrics",
        params={"region": region}
    )


async def get_earnings_quality_score(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> Dict[str, Any]:
    """Get earnings quality score and detailed information.

    Endpoint: /stock/earnings-quality-score

    Args:
        symbol: Stock symbol
        freq: Frequency - 'annual' or 'quarterly' (default: 'quarterly')

    Returns:
        Earnings quality score data
    """
    return await api_client.get(
        "/stock/earnings-quality-score",
        params={"symbol": symbol, "freq": freq}
    )


__all__ = [
    "get_basic_financials",
    "get_financials",
    "get_financials_reported",
    "get_sector_metrics",
    "get_earnings_quality_score",
]
