"""Finnhub API handlers package.

This package provides organized handler functions for all Finnhub API endpoints.
Based on Finnhub API documentation: https://finnhub.io/docs/api

All handlers are standalone async functions that import api_client internally.

Example:
    >>> from worker.config.handlers import analyst, company
    >>>
    >>> # Get company profile
    >>> profile = await company.get_company_profile2("AAPL")
    >>>
    >>> # Get analyst recommendations
    >>> recs = await analyst.get_recommendation_trends("AAPL")
"""

from . import analyst
from . import company
from . import earnings
from . import financials
from . import market
from . import news
from . import ownership
from . import trading

# Import all functions for direct access
from .analyst import (
    get_recommendation_trends,
    get_price_target,
    get_upgrade_downgrade,
    get_revenue_estimate,
    get_eps_estimate,
    get_ebitda_estimate,
    get_ebit_estimate,
)

from .company import (
    get_company_profile,
    get_company_profile2,
    get_company_peers,
    get_executive,
    get_historical_employee_count,
    get_filings,
    get_price_metrics,
    get_historical_market_cap,
)

from .earnings import (
    get_earnings,
    get_earnings_calendar,
)

from .financials import (
    get_basic_financials,
    get_financials,
    get_financials_reported,
    get_sector_metrics,
    get_earnings_quality_score,
)

from .market import (
    get_symbol_lookup,
    get_stock_symbols,
    get_market_status,
    get_market_holiday,
    get_quote,
    get_candles,
    get_technical_indicators,
)

from .news import (
    get_general_news,
    get_company_news,
    get_press_releases,
)

from .ownership import (
    get_ownership,
    get_fund_ownership,
    get_institutional_profile,
    get_institutional_portfolio,
    get_institutional_ownership,
    get_insider_transactions,
)

from .trading import (
    get_ipo_calendar,
    get_dividends,
    get_splits,
)


__all__ = [
    # Modules
    "analyst",
    "company",
    "earnings",
    "financials",
    "market",
    "news",
    "ownership",
    "trading",
    # Analyst functions
    "get_recommendation_trends",
    "get_price_target",
    "get_upgrade_downgrade",
    "get_revenue_estimate",
    "get_eps_estimate",
    "get_ebitda_estimate",
    "get_ebit_estimate",
    # Company functions
    "get_company_profile",
    "get_company_profile2",
    "get_company_peers",
    "get_executive",
    "get_historical_employee_count",
    "get_filings",
    "get_price_metrics",
    "get_historical_market_cap",
    # Earnings functions
    "get_earnings",
    "get_earnings_calendar",
    # Financials functions
    "get_basic_financials",
    "get_financials",
    "get_financials_reported",
    "get_sector_metrics",
    "get_earnings_quality_score",
    # Market functions
    "get_symbol_lookup",
    "get_stock_symbols",
    "get_market_status",
    "get_market_holiday",
    "get_quote",
    "get_candles",
    "get_technical_indicators",
    # News functions
    "get_general_news",
    "get_company_news",
    "get_press_releases",
    # Ownership functions
    "get_ownership",
    "get_fund_ownership",
    "get_institutional_profile",
    "get_institutional_portfolio",
    "get_institutional_ownership",
    "get_insider_transactions",
    # Trading functions
    "get_ipo_calendar",
    "get_dividends",
    "get_splits",
]
