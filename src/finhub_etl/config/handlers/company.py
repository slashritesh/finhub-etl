"""Company data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Optional, List, Dict, Any
from finhub_etl.config.finhub import api_client


async def get_company_profile(symbol: str) -> Dict[str, Any]:
    """Get general information of a company (v1).

    Endpoint: /stock/profile

    Args:
        symbol: Stock symbol (e.g., 'AAPL')

    Returns:
        Company profile data (v1)
    """
    return await api_client.get("/stock/profile", params={"symbol": symbol})


async def get_company_profile2(symbol: str) -> Dict[str, Any]:
    """Get general information of a company (v2 - recommended).

    Endpoint: /stock/profile2

    Args:
        symbol: Stock symbol (e.g., 'AAPL')

    Returns:
        Company profile data (v2)
    """
    return await api_client.get("/stock/profile2", params={"symbol": symbol})


async def get_company_peers(symbol: str) -> List[str]:
    """Get company peers in the same country and GICS sub-industry.

    Endpoint: /stock/peers

    Args:
        symbol: Stock symbol

    Returns:
        List of peer symbols
    """
    return await api_client.get("/stock/peers", params={"symbol": symbol})


async def get_executive(symbol: str) -> Dict[str, Any]:
    """Get company executive information.

    Endpoint: /stock/executive

    Args:
        symbol: Stock symbol

    Returns:
        Executive compensation and information
    """
    return await api_client.get("/stock/executive", params={"symbol": symbol})


async def get_historical_employee_count(symbol: str) -> Dict[str, Any]:
    """Get historical employee count data.

    Endpoint: /stock/historical-employee-count

    Args:
        symbol: Stock symbol

    Returns:
        Historical employee count data
    """
    return await api_client.get(
        "/stock/historical-employee-count",
        params={"symbol": symbol}
    )


async def get_filings(
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    form: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get SEC filings for a company.

    Endpoint: /stock/filings

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)
        form: Filter by form type (e.g., '10-K', '10-Q')

    Returns:
        List of SEC filings
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if form:
        params["form"] = form
    return await api_client.get("/stock/filings", params=params)


async def get_price_metrics(
    symbol: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """Get stock price metrics (intraday and period metrics).

    Endpoint: /stock/price-metric

    Args:
        symbol: Stock symbol
        date: Date in YYYY-MM-DD format (optional, defaults to current)

    Returns:
        Price metrics including 52-week high/low, beta, moving averages, etc.
    """
    params = {"symbol": symbol}
    if date:
        params["date"] = date
    return await api_client.get("/stock/price-metric", params=params)


async def get_historical_market_cap(
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get historical market capitalization data.

    Endpoint: /stock/historical-market-cap

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        Historical market cap data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/stock/historical-market-cap", params=params)


__all__ = [
    "get_company_profile",
    "get_company_profile2",
    "get_company_peers",
    "get_executive",
    "get_historical_employee_count",
    "get_filings",
    "get_price_metrics",
    "get_historical_market_cap",
]
