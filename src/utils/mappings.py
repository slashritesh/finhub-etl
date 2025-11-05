"""
Example mapping configurations for ETL operations.

This module provides example configurations for fetching and storing data
from Finnhub API to the database using the ETL utilities.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

from config import (
    get_company_profile,
    get_company_news,
    get_quote,
    get_stock_candles,
    get_peers,
    get_basic_financials,
    get_revenue_estimates,
    get_eps_estimates,
    get_recommendation_trends,
    get_dividends,
    get_insider_transactions,
)
from models.company import CompanyProfile
from models.news import CompanyNews
from models.market_data import StockQuote, StockCandle
from models.company_data import CompanyPeer
from models.financials import BasicFinancials
from models.earnings import RevenueEstimate, EpsEstimate
from models.recommendations import RecommendationTrend
from models.corporate_actions import Dividend
from models.ownership import InsiderTransaction
from utils.etl import (
    transform_candles_response,
    transform_peers_response,
    transform_estimates_response,
)


def get_company_data_mappings(symbol: str) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching complete company data.

    Args:
        symbol: Stock symbol (e.g., 'AAPL')

    Returns:
        List of mapping configurations
    """
    return [
        {
            'name': f'{symbol}_profile',
            'handler_func': get_company_profile,
            'model_class': CompanyProfile,
            'handler_params': {'symbol': symbol},
        },
        {
            'name': f'{symbol}_quote',
            'handler_func': get_quote,
            'model_class': StockQuote,
            'handler_params': {'symbol': symbol},
            'extra_fields': {'symbol': symbol},
        },
        {
            'name': f'{symbol}_peers',
            'handler_func': get_peers,
            'model_class': CompanyPeer,
            'handler_params': {'symbol': symbol},
            'transform_func': lambda data: transform_peers_response(data, symbol),
        },
        {
            'name': f'{symbol}_basic_financials',
            'handler_func': get_basic_financials,
            'model_class': BasicFinancials,
            'handler_params': {'symbol': symbol},
            'extra_fields': {'symbol': symbol},
        },
    ]


def get_news_mappings(symbol: str, days_back: int = 30) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching news data.

    Args:
        symbol: Stock symbol
        days_back: Number of days to look back for news

    Returns:
        List of mapping configurations
    """
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    return [
        {
            'name': f'{symbol}_news',
            'handler_func': get_company_news,
            'model_class': CompanyNews,
            'handler_params': {
                'symbol': symbol,
                'from_date': from_date,
                'to_date': to_date,
            },
            'extra_fields': {'symbol': symbol},
        },
    ]


def get_market_data_mappings(
    symbol: str,
    resolution: str = 'D',
    days_back: int = 30
) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching market data (candles).

    Args:
        symbol: Stock symbol
        resolution: Candle resolution ('1', '5', '15', '30', '60', 'D', 'W', 'M')
        days_back: Number of days to look back

    Returns:
        List of mapping configurations
    """
    to_timestamp = int(datetime.now().timestamp())
    from_timestamp = int((datetime.now() - timedelta(days=days_back)).timestamp())

    return [
        {
            'name': f'{symbol}_candles_{resolution}',
            'handler_func': get_stock_candles,
            'model_class': StockCandle,
            'handler_params': {
                'symbol': symbol,
                'resolution': resolution,
                'from_timestamp': from_timestamp,
                'to_timestamp': to_timestamp,
            },
            'transform_func': lambda data: transform_candles_response(data, symbol, resolution),
        },
    ]


def get_estimates_mappings(symbol: str, freq: str = 'annual') -> List[Dict[str, Any]]:
    """
    Get mappings for fetching earnings estimates.

    Args:
        symbol: Stock symbol
        freq: Frequency ('annual' or 'quarterly')

    Returns:
        List of mapping configurations
    """
    return [
        {
            'name': f'{symbol}_revenue_estimates',
            'handler_func': get_revenue_estimates,
            'model_class': RevenueEstimate,
            'handler_params': {'symbol': symbol, 'freq': freq},
            'transform_func': transform_estimates_response,
            'extra_fields': {'symbol': symbol, 'freq': freq},
        },
        {
            'name': f'{symbol}_eps_estimates',
            'handler_func': get_eps_estimates,
            'model_class': EpsEstimate,
            'handler_params': {'symbol': symbol, 'freq': freq},
            'transform_func': transform_estimates_response,
            'extra_fields': {'symbol': symbol, 'freq': freq},
        },
    ]


def get_analyst_data_mappings(symbol: str) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching analyst data.

    Args:
        symbol: Stock symbol

    Returns:
        List of mapping configurations
    """
    return [
        {
            'name': f'{symbol}_recommendations',
            'handler_func': get_recommendation_trends,
            'model_class': RecommendationTrend,
            'handler_params': {'symbol': symbol},
            'extra_fields': {'symbol': symbol},
        },
    ]


def get_corporate_actions_mappings(
    symbol: str,
    days_back: int = 365
) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching corporate actions (dividends).

    Args:
        symbol: Stock symbol
        days_back: Number of days to look back

    Returns:
        List of mapping configurations
    """
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    return [
        {
            'name': f'{symbol}_dividends',
            'handler_func': get_dividends,
            'model_class': Dividend,
            'handler_params': {
                'symbol': symbol,
                'from_date': from_date,
                'to_date': to_date,
            },
        },
    ]


def get_ownership_mappings(symbol: str, days_back: int = 365) -> List[Dict[str, Any]]:
    """
    Get mappings for fetching ownership data.

    Args:
        symbol: Stock symbol
        days_back: Number of days to look back

    Returns:
        List of mapping configurations
    """
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    return [
        {
            'name': f'{symbol}_insider_transactions',
            'handler_func': get_insider_transactions,
            'model_class': InsiderTransaction,
            'handler_params': {
                'symbol': symbol,
                'from_date': from_date,
                'to_date': to_date,
            },
        },
    ]


def get_full_company_mappings(symbol: str) -> List[Dict[str, Any]]:
    """
    Get all available mappings for a company.

    Args:
        symbol: Stock symbol

    Returns:
        Combined list of all mapping configurations
    """
    mappings = []
    mappings.extend(get_company_data_mappings(symbol))
    mappings.extend(get_news_mappings(symbol, days_back=30))
    mappings.extend(get_market_data_mappings(symbol, resolution='D', days_back=30))
    mappings.extend(get_estimates_mappings(symbol))
    mappings.extend(get_analyst_data_mappings(symbol))
    mappings.extend(get_corporate_actions_mappings(symbol))
    mappings.extend(get_ownership_mappings(symbol))

    return mappings


# Example usage configuration
EXAMPLE_MAPPINGS = {
    'AAPL': get_full_company_mappings('AAPL'),
    'GOOGL': get_full_company_mappings('GOOGL'),
    'MSFT': get_full_company_mappings('MSFT'),
}
