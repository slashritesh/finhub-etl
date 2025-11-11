"""Other miscellaneous handlers"""
from ..finhub import api_client


async def get_company_dividends(symbol: str, from_date: str = None, to_date: str = None):
    """Fetch dividend history for a given company symbol.
    Args:
        symbol (str): Stock ticker symbol
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Dividend data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/dividend", params=params)


async def get_company_price_metrics(symbol: str):
    """Fetch price-performance metrics for a given company.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        dict: Price metrics data
    """
    return await api_client.get("/stock/price-metric", params={"symbol": symbol})


async def get_sector_metrics(region: str = None):
    """Fetch sector-level performance & ratio metrics.
    Args:
        region (str, optional): Region code (e.g., 'US', 'EU')
    Returns:
        dict: Sector metrics data
    """
    params = {}
    if region:
        params["region"] = region
    return await api_client.get("/sector/metrics", params=params)


async def get_ipo_calendar(from_date: str, to_date: str):
    """Fetch IPO calendar data between two dates.
    Args:
        from_date (str): Start date in YYYY-MM-DD format
        to_date (str): End date in YYYY-MM-DD format
    Returns:
        dict: IPO calendar data
    """
    return await api_client.get("/calendar/ipo", params={"from": from_date, "to": to_date})


async def get_historical_mcap(symbol: str, from_date: str = None, to_date: str = None):
    """Fetch historical market-capitalization data.
    Args:
        symbol (str): Stock ticker symbol
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Historical market cap data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/historical-market-cap", params=params)


async def get_insider_transactions(
    symbol: str, from_date: str = None, to_date: str = None
):
    """Fetch insider transactions for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        dict: Insider transactions data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/insider-transactions", params=params)


async def get_company_filings(
    symbol: str = None,
    cik: str = None,
    access_number: str = None,
    from_date: str = None,
    to_date: str = None,
):
    """Fetch company filings.
    Args:
        symbol (str, optional): Stock ticker symbol
        cik (str, optional): CIK code
        access_number (str, optional): Access number
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Company filings data
    """
    params = {}
    if symbol:
        params["symbol"] = symbol
    if cik:
        params["cik"] = cik
    if access_number:
        params["accessNumber"] = access_number
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/filings", params=params)


async def get_historical_employee_count(symbol: str):
    """Fetch historical employee count for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        dict: Historical employee count data
    """
    return await api_client.get(
        "/stock/historical-employee-count", params={"symbol": symbol}
    )
