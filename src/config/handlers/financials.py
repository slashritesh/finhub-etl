"""Financial data handlers"""
from ..finhub import api_client


async def get_company_basic_financials(symbol: str, metric: str = "all"):
    """Fetch basic financials for a given company.
    Args:
        symbol (str): Stock ticker symbol
        metric (str): Metric type (all, price, valuation, margin)
    Returns:
        dict: Basic financials data
    """
    return await api_client.get(
        "/stock/metric", params={"symbol": symbol, "metric": metric}
    )


async def get_company_financials(symbol: str, statement: str, freq: str = "annual"):
    """Fetch standardized financial statements for a given company.
    Args:
        symbol (str): Stock ticker symbol
        statement (str): Type of statement (income, balance_sheet, cash_flow)
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: Financial statements data
    """
    return await api_client.get(
        "/stock/financials",
        params={"symbol": symbol, "statement": statement, "freq": freq},
    )


async def get_company_reported_financials(symbol: str):
    """Fetch financials as reported for a given company.
    Args:
        symbol (str): Stock ticker symbol
    Returns:
        dict: Reported financials data
    """
    return await api_client.get("/stock/financials-reported", params={"symbol": symbol})
