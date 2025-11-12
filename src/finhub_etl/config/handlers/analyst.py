"""Analyst data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, List, Optional
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
) -> List[Dict[str, Any]]:  # <-- IMPORTANT: Return type is now a List
    """
    Get revenue estimates.

    This handler transforms the raw API response into the flat list
    format expected by the generic save function.
    """
    # 1. Fetch the raw data from the API client
    raw_response = await api_client.get(
        "/stock/revenue-estimate",
        params={"symbol": symbol, "freq": freq}
    )

    # 2. Check for empty or invalid responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of records from the 'data' key
    records_list = raw_response["data"]

    # 4. Enrich each record with the symbol (for the composite primary key)
    #    This is the most important step.
    for record in records_list:
        record["symbol"] = symbol

    # 5. Return the clean, flat list
    return records_list


async def get_eps_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> List[Dict[str, Any]]:  # <-- Change return type to List
    """Get EPS (earnings per share) estimates.

    This handler transforms the raw API response into the flat list
    format expected by the generic save function.
    """
    # 1. Fetch the raw data
    raw_response = await api_client.get(
        "/stock/eps-estimate",
        params={"symbol": symbol, "freq": freq}
    )

    # 2. Handle empty responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of records
    records_list = raw_response["data"]

    # 4. Add the symbol to each record
    for record in records_list:
        record["symbol"] = symbol

    # 5. Return the clean list
    return records_list


async def get_ebitda_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> List[Dict[str, Any]]:  # <-- Change return type to a List
    """Get EBITDA estimates.

    This handler transforms the raw API response into the flat list
    format expected by the generic save function.
    """
    # 1. Fetch the raw data
    raw_response = await api_client.get(
        "/stock/ebitda-estimate",
        params={"symbol": symbol, "freq": freq}
    )

    # 2. Handle empty responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of records
    records_list = raw_response["data"]

    # 4. Add the symbol to each record for the composite key
    for record in records_list:
        record["symbol"] = symbol

    # 5. Return the clean, ready-to-save list
    return records_list


async def get_ebit_estimate(
    symbol: str,
    freq: Optional[str] = "quarterly"
) -> List[Dict[str, Any]]:  # <-- Change return type to a List
    """Get EBIT estimates.

    This handler transforms the raw API response into the flat list
    format expected by the generic save function.
    """
    # 1. Fetch the raw data
    raw_response = await api_client.get(
        "/stock/ebit-estimate",
        params={"symbol": symbol, "freq": freq}
    )

    # 2. Handle empty responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list from the 'data' key
    records_list = raw_response["data"]

    # 4. Add the symbol to each record in the list
    for record in records_list:
        record["symbol"] = symbol

    # 5. Return the clean list
    return records_list


__all__ = [
    "get_recommendation_trends",
    "get_price_target",
    "get_upgrade_downgrade",
    "get_revenue_estimate",
    "get_eps_estimate",
    "get_ebitda_estimate",
    "get_ebit_estimate",
]
