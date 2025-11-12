"""Financial data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Dict, Any, List, Optional
from finhub_etl.config.finhub import api_client


async def get_basic_financials(
    symbol: str,
    metric: Optional[str] = "all"
) -> Dict[str, Any]: # <-- Returns a single, clean dictionary
    """
    Get basic financials and formats the response for storage.
    """
    # 1. Fetch the raw, complex response
    raw_response = await api_client.get(
        "/stock/metric",
        params={"symbol": symbol, "metric": metric}
    )

    # 2. Handle empty or malformed responses
    if not raw_response or "metric" not in raw_response:
        return {}

    # 3. Extract the main dictionary of metrics. This is our base.
    financial_data = raw_response["metric"]

    # 4. Add the top-level symbol and metricType to the dictionary
    financial_data["symbol"] = raw_response.get("symbol")
    financial_data["metricType"] = raw_response.get("metricType")

    # 5. Return the final, flattened dictionary ready for the model
    return financial_data


async def get_financials(
    symbol: str,
    statement: str,
    freq: str, # Changed to be required, as the API needs it
    preliminary: Optional[bool] = False # Added optional param from docs
) -> List[Dict[str, Any]]: # <-- The return type MUST be a List
    """
    Get standardized financials and formats the response for the CompanyFinancials model.
    """
    params = {
        "symbol": symbol,
        "statement": statement,
        "freq": freq,
        "preliminary": preliminary,
    }
    # Filter out any optional params that are not set
    active_params = {k: v for k, v in params.items() if v}

    # 1. Fetch the raw, nested response from the API
    raw_response = await api_client.get("/stock/financials", params=active_params)

    # 2. Handle empty or malformed responses
    if not raw_response or "financials" not in raw_response:
        return []

    # 3. Extract the list of financial records
    financials_list = raw_response["financials"]

    # 4. CRITICAL: Inject the necessary context into each record to match the model
    for record in financials_list:
        record["symbol"] = symbol
        record["frequency"] = freq          # Add the frequency
        record["statement_type"] = statement  # Add the statement type

    # 5. Return the clean, flat list ready for the database
    return financials_list


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
