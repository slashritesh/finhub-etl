"""Company data handlers for Finnhub API.

Reference: https://finnhub.io/docs/api
"""

from typing import Optional, List, Dict, Any
from finhub_etl.config.finhub import api_client


async def get_company_profile(
    symbol: str,
    isin: Optional[str] = None,
    cusip: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get general information of a company (v1).
    'symbol' is required. 'isin' and 'cusip' are optional.
    """
    # Create a dictionary of all possible parameters
    all_params = {"symbol": symbol, "isin": isin, "cusip": cusip}

    # Filter out any optional parameters that are None or empty strings
    active_params = {key: value for key, value in all_params.items() if value}

    # Make the API call with the active parameters
    return await api_client.get("/stock/profile", params=active_params)



async def get_company_profile2(
    symbol: str,
    isin: Optional[str] = None,
    cusip: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get general information of a company (v2 - recommended).
    'symbol' is required. 'isin' and 'cusip' are optional.
    """
    # Create a dictionary of all possible parameters
    all_params = {"symbol": symbol, "isin": isin, "cusip": cusip}

    # Filter out any optional parameters that are None or empty strings
    active_params = {key: value for key, value in all_params.items() if value}

    # Make the API call with the active parameters
    return await api_client.get("/stock/profile2", params=active_params)


async def get_company_peers(
    symbol: str,
    grouping: Optional[str] = None
) -> Dict[str, Any]: 
    """
    Get company peers and formats the response for database storage.

    Endpoint: /stock/peers
    """
    params: Dict[str, Any] = {"symbol": symbol}
    if grouping:
        params["grouping"] = grouping

    # 1. Fetch the list of peer symbols from the API
    peers_list = await api_client.get("/stock/peers", params=params)

    # 2. Check if the API returned a valid list
    if not isinstance(peers_list, list):
        # Return an empty dict if the API response is not what we expect
        return {}

    # 3. CRITICAL STEP: Combine the original symbol and the peer list
    return {
        "symbol": symbol,
        "peers": peers_list
    }


async def get_executive(symbol: str) -> List[Dict[str, Any]]:  # <-- Return type is now a List
    """
    Get company executive information and formats it for storage.

    Endpoint: /stock/executive
    """
    # 1. Fetch the raw, nested data from the API
    raw_response = await api_client.get("/stock/executive", params={"symbol": symbol})

    # 2. Handle cases where the response is empty or malformed
    if not raw_response or "executive" not in raw_response:
        return []

    # 3. Extract the list of executives
    executive_list = raw_response["executive"]

    # 4. CRITICAL STEP: Add the company symbol to each executive's record
    for executive in executive_list:
        executive["symbol"] = symbol

    # 5. Return the clean, flat list
    return executive_list


async def get_historical_employee_count(
    symbol: str,
    _from: str,  # Using _from because 'from' is a reserved keyword in Python
    to: str
) -> List[Dict[str, Any]]:  # <-- Return type is a List
    """
    Get historical employee count data and formats it for storage.
    """
    # 1. Fetch the raw data from the API with the required date params
    raw_response = await api_client.get(
        "/stock/historical-employee-count",
        params={"symbol": symbol, "from": _from, "to": to}
    )

    # 2. Handle empty or malformed responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of records
    records_list = raw_response["data"]
    
    # 4. Process each record to match the model's expectations
    processed_records = []
    for record in records_list:
        processed_records.append({
            "symbol": symbol,  # <-- Inject the symbol
            "period_date": record.get("atDate"),  # <-- Rename "atDate" to "period_date"
            "employee_count": record.get("employee"), # <-- Rename "employee" to "employee_count"
        })

    # 5. Return the clean, flat list of dictionaries
    return processed_records


async def get_filings(
    symbol: Optional[str] = None,
    cik: Optional[str] = None,
    accessNumber: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    form: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get SEC filings for a company.

    Endpoint: /stock/filings
    """
    # 1. Create a dictionary of all possible API parameters
    all_params = {
        "symbol": symbol,
        "cik": cik,
        "accessNumber": accessNumber,
        "from": from_date,
        "to": to_date,
        "form": form,
    }

    # 2. Filter out any parameters that are None or empty strings
    active_params = {key: value for key, value in all_params.items() if value}

    # 3. Make the API call with only the provided parameters
    return await api_client.get("/stock/filings", params=active_params)


async def get_price_metrics(
    symbol: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get stock price metrics and formats the response for storage.
    """
    params = {"symbol": symbol}
    if date:
        params["date"] = date

    # 1. Fetch the raw, nested data
    raw_response = await api_client.get("/stock/price-metric", params=params)

    # 2. Handle empty or malformed responses
    if not raw_response or "data" not in raw_response:
        return {}

    # 3. Extract the dictionary of metrics from the 'data' key
    metrics_data = raw_response["data"]

    # 4. Add the symbol to that dictionary
    metrics_data["symbol"] = symbol

    # 5. Return the single, clean dictionary
    return metrics_data


async def get_historical_market_cap(
    symbol: str,
    from_date: str, # Changed to be required
    to_date: str    # Changed to be required
) -> List[Dict[str, Any]]:  # <-- Return type is a List
    """
    Get historical market cap data and formats it for storage.
    """
    # 1. Fetch the raw data from the API with the required date params
    raw_response = await api_client.get(
        "/stock/historical-market-cap",
        params={"symbol": symbol, "from": from_date, "to": to_date}
    )

    # 2. Handle empty or malformed responses
    if not raw_response or "data" not in raw_response:
        return []

    # 3. Extract the list of records
    records_list = raw_response["data"]
    
    # 4. Process each record to match the model's expectations
    processed_records = []
    for record in records_list:
        processed_records.append({
            "symbol": symbol,  # <-- Inject the symbol
            "date": record.get("atDate"),  # <-- Rename "atDate" to "date"
            "market_cap": record.get("marketCapitalization"), # <-- Rename "marketCapitalization"
        })

    # 5. Return the clean, flat list of dictionaries
    return processed_records


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
