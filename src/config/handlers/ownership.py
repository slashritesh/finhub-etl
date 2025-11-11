"""Ownership-related handlers"""
from ..finhub import api_client


async def get_company_ownership(
    symbol: str = None, cusip: str = None, from_date: str = None, to_date: str = None
):
    """Fetch full list of shareholders of a company over time.
    Args:
        symbol (str, optional): Stock ticker symbol
        cusip (str, optional): CUSIP code
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Ownership records
    """
    params = {}
    if symbol:
        params["symbol"] = symbol
    if cusip:
        params["cusip"] = cusip
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    result = await api_client.get("/stock/ownership", params=params)

    if not result or "ownership" not in result:
        return []

    ownership_records = []
    for record in result["ownership"]:
        ownership_records.append(
            {
                "symbol": result.get("symbol", symbol),
                "name": record.get("name"),
                "change": record.get("change"),
                "filingDate": record.get("filingDate"),
                "share": record.get("share"),
            }
        )

    return ownership_records


async def get_fund_ownership(symbol: str, from_date: str = None, to_date: str = None):
    """Fetch the fund ownership for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        dict: Fund ownership data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/fund-ownership", params=params)


async def get_institutional_ownership(
    symbol: str = None, cusip: str = None, from_date: str = None, to_date: str = None
):
    """Fetch institutional investors' positions in a given stock over time.
    Args:
        symbol (str, optional): Stock ticker symbol
        cusip (str, optional): CUSIP code
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        dict: Institutional ownership data
    """
    params = {}
    if symbol:
        params["symbol"] = symbol
    if cusip:
        params["cusip"] = cusip
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/institutional/ownership", params=params)
