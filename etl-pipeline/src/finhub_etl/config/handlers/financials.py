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

async def get_financials_reported(symbol: str, freq: Optional[str] = "annual") -> List[Dict[str, Any]]:
    """
    Fetch and flatten financials-reported data so each filing is a DB-ready dict.
    """
    raw = await api_client.get(
        "/stock/financials-reported",
        params={"symbol": symbol, "freq": freq}
    )

    filings = []

    for item in raw.get("data", []):
        filings.append({
            "symbol": item["symbol"],
            "cik": item["cik"],
            "access_number": item["accessNumber"],
            "year": item.get("year"),
            "quarter": item.get("quarter"),
            "form": item.get("form"),
            "start_date": item.get("startDate"),
            "end_date": item.get("endDate"),
            "filed_date": item.get("filedDate"),
            "accepted_date": item.get("acceptedDate"),
            "report": item.get("report")  # JSON blob to store
        })

    return filings



async def get_sector_metrics(region: str) -> List[Dict[str, Any]]:
    """Get sector metrics including performance, valuation, and financial ratios.

    Endpoint: /sector/metrics

    Args:
        region: Region code (e.g., 'NA')

    Returns:
        List of sectors with metrics in the format:
        {
            "sector": str,
            "region": str,
            "metrics": dict
        }
    """
    data = await api_client.get(
        "/sector/metrics",
        params={"region": region}
    )

    sectors = data.get("data", [])

    result = []
    for item in sectors:
        result.append({
            "sector": item.get("sector"),
            "region": region,
            "metrics": item.get("metrics", {})
        })

    return result


async def get_earnings_quality_score(
    symbol: str,
    freq: str # This is a required parameter according to the docs
) -> List[Dict[str, Any]]: # <-- The return type MUST be a List
    """
    Get earnings quality score and formats the data for storage.
    """
    params = {"symbol": symbol, "freq": freq}
        
    # 1. Fetch the raw, nested response from the API
    raw_response = await api_client.get(
        "/stock/earnings-quality-score",
        params=params
    )

    # 2. Handle empty or malformed responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of score records
    score_list = raw_response["data"]

    # 4. CRITICAL: Inject the symbol and frequency into each record
    for record in score_list:
        record["symbol"] = symbol
        record["freq"] = freq

    # 5. Return the clean, flat list ready for the database
    return score_list


__all__ = [
    "get_basic_financials",
    "get_financials",
    "get_financials_reported",
    "get_sector_metrics",
    "get_earnings_quality_score",
]
