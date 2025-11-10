from .finhub import api_client


async def get_stock_symbols(exchange):
    """Get all stock symbols for a given exchange.
    Args:
        exchange (str): Exchange code (e.g., 'US', 'TO', 'L')
    Returns:
        list: List of stock symbols on the exchange
    """
    return await api_client.get("/stock/symbol", params={"exchange": exchange})


async def get_company_profile(symbol: str = None, isin: str = None, cusip: str = None) -> dict:
    """Fetch the full company profile for a given company.
    Args:
        symbol (str, optional): Stock ticker symbol (e.g., 'AAPL').
        isin (str, optional): ISIN code of the company.
        cusip (str, optional): CUSIP code of the company.
    Returns:
        dict: Company profile data
    """
    params = {}
    if symbol:
        params["symbol"] = symbol
    if isin:
        params["isin"] = isin
    if cusip:
        params["cusip"] = cusip

    return await api_client.get("/stock/profile", params=params)


async def get_company_profile2(symbol: str) -> dict:
    """Fetch the company profile for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    Returns:
        dict: Company profile data
    """
    return await api_client.get("/stock/profile2", params={"symbol": symbol})


async def get_company_news(symbol: str, from_date: str, to_date: str) :
    """
    Fetch company-specific news for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        from_date (str): Start date in YYYY-MM-DD format (e.g., '2024-01-01')
        to_date (str): End date in YYYY-MM-DD format (e.g., '2024-12-31')
    Returns:
        list: List of news articles (JSON objects)
    """
    return await api_client.get(
        "/company-news", params={"symbol": symbol, "from": from_date, "to": to_date}
    )


async def get_company_peers(symbol: str) -> list :
    """
    Fetch peer companies for a given company symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
    Returns:
        list: List of ticker symbols of peer companies
    """
    return await api_client.get("/stock/peers", params={"symbol": symbol})


async def get_press_release(
    symbol: str, from_date: str = None, to_date: str = None
) :
    """
    Fetch press releases for a given company symbol.
    Args:
        symbol (str): Stock ticker (e.g., 'AAPL')
        from_date (str, optional): Start date 'YYYY-MM-DD'
        to_date (str, optional): End date 'YYYY-MM-DD'
    Returns:
        list: List of press-release entries (JSON objects)
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/press-releases2", params=params)


async def get_company_ownership(
    symbol: str = None, cusip: str = None, from_date: str = None, to_date: str = None
) -> dict :
    """
    Fetch full list of shareholders (institutional + other) of a company over time.
    Args:
        symbol (str, optional): Stock ticker symbol (e.g., 'AAPL')
        cusip (str, optional): CUSIP code of the company
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Ownership entries
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

    return await api_client.get("/stock/ownership", params=params)


async def get_fund_ownership(
    symbol: str, from_date: str = None, to_date: str = None
) :
    """
    Fetch the fund ownership for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Fund ownership entries
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/fund-ownership", params=params)


async def get_institutional_profile(cik: str = None) :
    """
    Fetch institutional investor profiles (well-known institutions).
    Args:
        cik (str, optional): CIK of the institution. If omitted, fetch list of all supported institutions.
    Returns:
        list: Institution profile entries
    """
    params = {}
    if cik:
        params["cik"] = cik

    return await api_client.get("/institutional/profile", params=params)


async def get_institutional_portfolio(
    cik: str, from_date: str = None, to_date: str = None
) :
    """
    Fetch institutional investor portfolio holdings from 13-F filings.
    Args:
        cik (str): CIK of the institution
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Portfolio holdings entries
    """
    params = {"cik": cik}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/institutional/portfolio", params=params)


async def get_institutional_ownership(
    symbol: str = None, cusip: str = None, from_date: str = None, to_date: str = None
) :
    """
    Fetch institutional investors' positions in a given stock over time (13-F source).
    Args:
        symbol (str, optional): Stock ticker symbol
        cusip (str, optional): CUSIP code
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        list: Institutional ownership entries
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


async def get_company_basic_financials(symbol: str, metric: str = "all") :
    """
    Fetch basic financials for a given company.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        metric (str): Metric type, e.g., 'all', 'price', 'valuation', 'margin'. :contentReference[oaicite:1]{index=1}
    Returns:
        dict: Basic financials data
    """
    return await api_client.get(
        "/stock/metric", params={"symbol": symbol, "metric": metric}
    )
    # Note: Some docs call this /company_basic_financials endpoint. :contentReference[oaicite:2]{index=2}


async def get_company_financials(
    symbol: str, statement: str, freq: str = "annual"
) :
    """
    Fetch standardized financial statements for a given company.
    Args:
        symbol (str): Stock ticker symbol.
        statement (str): Type of statement e.g., 'income', 'balance_sheet', 'cash_flow'. :contentReference[oaicite:3]{index=3}
        freq (str): Frequency of the statement — 'annual' or 'quarterly'.
    Returns:
        dict: Financial statements data
    """
    return await api_client.get(
        "/stock/financials",
        params={"symbol": symbol, "statement": statement, "freq": freq},
    )


async def get_company_reported_financials(symbol: str):
    """
    Fetch financials as reported (original filings) for a given company.
    Args:
        symbol (str): Stock ticker symbol.
    Returns:
        dict: Reported financials data
    """
    return await api_client.get("/stock/financials-reported", params={"symbol": symbol})
    # This endpoint provides standardized balance sheet, income statement, cash flow for 30+ years



async def get_company_dividends(symbol: str, from_date: str = None, to_date: str = None) :
    """
    Fetch dividend history for a given company symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., "AAPL")
        from_date (str, optional): Start date in "YYYY-MM-DD" format
        to_date (str, optional): End date in "YYYY-MM-DD" format
    Returns:
        list: List of dividend entries
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    
    return await api_client.get(
        "/stock/dividend",
        params=params
    )


async def get_company_price_metrics(symbol: str) :
    """
    Fetch price-performance metrics for a given company.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
    Returns:
        dict: Price metrics (e.g., 52-week high/low, YTD return, etc)
    """
    return await api_client.get("/stock/price-metric", params={"symbol": symbol})



async def get_sector_metrics(region: str = None) :
    """
    Fetch sector-level performance & ratio metrics.
    Args:
        region (str, optional): Region code or index to filter sector metrics (e.g., 'US', 'EU')
    Returns:
        dict: Sector metrics data
    """
    params = {}
    if region:
        params["region"] = region
    return await api_client.get("/sector/metrics", params=params)


async def get_ipo_calendar(from_date: str, to_date: str) :
    """
    Fetch IPO calendar data between two dates.
    Args:
        from_date (str): Start date, format 'YYYY-MM-DD'
        to_date (str): End date, format 'YYYY-MM-DD'
    Returns:
        list: IPO calendar entries (recent and upcoming IPOs)
    """
    return await api_client.get("/calendar/ipo", params={"from": from_date, "to": to_date})


async def get_historical_mcap(symbol: str, from_date: str = None, to_date: str = None) :
    """
    Fetch historical market-capitalization data for a given company symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
        from_date (str, optional): Start date in 'YYYY-MM-DD' format
        to_date (str, optional): End date in 'YYYY-MM-DD' format
    Returns:
        list: A list of market-cap entries (date + value)
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/stock/historical-market-cap", params=params)
