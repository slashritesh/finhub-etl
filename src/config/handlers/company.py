"""Company-related handlers"""
from ..finhub import api_client


async def get_stock_symbols(exchange: str):
    """Get all stock symbols for a given exchange.
    Args:
        exchange (str): Exchange code (e.g., 'US', 'TO', 'L')
    Returns:
        list: List of stock symbols on the exchange
    """
    return await api_client.get("/stock/symbol", params={"exchange": exchange})


async def get_company_profile(symbol: str = None, isin: str = None, cusip: str = None):
    """Fetch the full company profile for a given company.
    Args:
        symbol (str, optional): Stock ticker symbol (e.g., 'AAPL')
        isin (str, optional): ISIN code of the company
        cusip (str, optional): CUSIP code of the company
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


async def get_company_profile2(symbol: str):
    """Fetch the company profile for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    Returns:
        dict: Company profile data
    """
    return await api_client.get("/stock/profile2", params={"symbol": symbol})


async def get_company_peers(symbol: str):
    """Fetch peer companies for a given company symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
    Returns:
        dict: Peer companies data with symbol
    """
    result = await api_client.get("/stock/peers", params={"symbol": symbol})
    return {"symbol": symbol, "peers": result}


async def get_company_executives(symbol: str):
    """Fetch company executives for a given symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g., 'AAPL')
    Returns:
        list: List of company executives
    """
    return await api_client.get("/stock/executive", params={"symbol": symbol})
