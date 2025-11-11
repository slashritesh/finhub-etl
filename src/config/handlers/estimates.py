"""Financial estimates handlers"""
from ..finhub import api_client


async def get_revenue_estimate(symbol: str, freq: str = "annual"):
    """Fetch revenue estimates for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: Revenue estimate data
    """
    return await api_client.get(
        "/stock/revenue-estimate", params={"symbol": symbol, "freq": freq}
    )


async def get_eps_estimate(symbol: str, freq: str = "annual"):
    """Fetch EPS estimates for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: EPS estimate data
    """
    return await api_client.get(
        "/stock/eps-estimate", params={"symbol": symbol, "freq": freq}
    )


async def get_ebitda_estimate(symbol: str, freq: str = "annual"):
    """Fetch EBITDA estimates for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: EBITDA estimate data
    """
    return await api_client.get(
        "/stock/ebitda-estimate", params={"symbol": symbol, "freq": freq}
    )


async def get_ebit_estimate(symbol: str, freq: str = "annual"):
    """Fetch EBIT estimates for a given symbol.
    Args:
        symbol (str): Stock ticker symbol
        freq (str): Frequency (annual, quarterly)
    Returns:
        dict: EBIT estimate data
    """
    return await api_client.get(
        "/stock/ebit-estimate", params={"symbol": symbol, "freq": freq}
    )
