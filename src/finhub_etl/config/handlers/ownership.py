"""Ownership and institutional data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, List, Optional
from finhub_etl.config.finhub import api_client


async def get_ownership(
    symbol: str,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """Get shareholder ownership data.

    Endpoint: /stock/ownership

    Args:
        symbol: Stock symbol
        limit: Number of results (optional)

    Returns:
        Ownership breakdown data
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    return await api_client.get("/stock/ownership", params=params)


async def get_fund_ownership(
    symbol: str,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]: # <-- The return type MUST be a List
    """
    Get mutual fund ownership data and formats it for storage.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
        
    # 1. Fetch the raw, nested response from the API
    raw_response = await api_client.get("/stock/fund-ownership", params=params)

    # 2. Handle empty or malformed responses
    if not raw_response or "ownership" not in raw_response:
        return []

    # 3. Extract the list of ownership records
    ownership_list = raw_response["ownership"]

    # 4. CRITICAL: Inject the symbol into each record
    for record in ownership_list:
        record["symbol"] = symbol

    # 5. Return the clean, flat list ready for the database
    return ownership_list


async def get_institutional_profile(
    cik: Optional[str] = None
) -> List[Dict[str, Any]]: # <-- Return type is a List
    """
    Get institutional profile information.

    Endpoint: /institutional/profile
    """
    params = {}
    if cik:
        params["cik"] = cik
        
    # 1. Fetch the raw, nested response from the API
    raw_response = await api_client.get("/institutional/profile", params=params)

    # 2. Handle empty or malformed responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract and return the clean list of profile data.
    #    The 'cik' is already inside each record, so no extra processing is needed.
    return raw_response["data"]


async def get_institutional_portfolio(
    cik: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get institutional portfolio holdings.

    Endpoint: /institutional/portfolio

    Args:
        cik: Institution's CIK number
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        Portfolio holdings data
    """
    params = {"cik": cik}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/institutional/portfolio", params=params)


async def get_institutional_ownership(
    symbol: str,
    cusip: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get institutional ownership data for a stock.

    Endpoint: /institutional/ownership

    Args:
        symbol: Stock symbol
        cusip: CUSIP number (optional)
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        Institutional ownership data
    """
    params = {"symbol": symbol}
    if cusip:
        params["cusip"] = cusip
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/institutional/ownership", params=params)


async def get_insider_transactions(
    symbol: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get insider transactions.

    Endpoint: /stock/insider-transactions

    Args:
        symbol: Stock symbol
        from_date: Start date (YYYY-MM-DD)
        to_date: End date (YYYY-MM-DD)

    Returns:
        Insider transaction data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/stock/insider-transactions", params=params)


__all__ = [
    "get_ownership",
    "get_fund_ownership",
    "get_institutional_profile",
    "get_institutional_portfolio",
    "get_institutional_ownership",
    "get_insider_transactions",
]
