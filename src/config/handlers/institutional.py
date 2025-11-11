"""Institutional investor handlers"""
from ..finhub import api_client


async def get_institutional_profile(cik: str = None):
    """Fetch institutional investor profiles.
    Args:
        cik (str, optional): CIK of the institution
    Returns:
        dict: Institution profile data
    """
    params = {}
    if cik:
        params["cik"] = cik

    return await api_client.get("/institutional/profile", params=params)


async def get_institutional_portfolio(
    cik: str, from_date: str = None, to_date: str = None
):
    """Fetch institutional investor portfolio holdings from 13-F filings.
    Args:
        cik (str): CIK of the institution
        from_date (str, optional): Start date in YYYY-MM-DD format
        to_date (str, optional): End date in YYYY-MM-DD format
    Returns:
        dict: Portfolio holdings data
    """
    params = {"cik": cik}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    return await api_client.get("/institutional/portfolio", params=params)
