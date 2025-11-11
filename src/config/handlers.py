"""
Legacy handlers import - redirects to new handlers package
For backward compatibility
"""

from .handlers import *

__all__ = [
    # Company
    "get_stock_symbols",
    "get_company_profile",
    "get_company_profile2",
    "get_company_peers",
    "get_company_executives",
    # News
    "get_company_news",
    "get_general_news",
    "get_press_release",
    # Ownership
    "get_company_ownership",
    "get_fund_ownership",
    "get_institutional_ownership",
    # Institutional
    "get_institutional_profile",
    "get_institutional_portfolio",
    # Financials
    "get_company_basic_financials",
    "get_company_financials",
    "get_company_reported_financials",
    # Market
    "get_market_status",
    "get_market_holidays",
    "get_realtime_quote",
    # Analyst
    "get_analyst_recommendations",
    "get_price_target",
    "get_upgrade_downgrade",
    # Estimates
    "get_revenue_estimate",
    "get_eps_estimate",
    "get_ebitda_estimate",
    "get_ebit_estimate",
    # Earnings
    "get_earnings_data",
    "get_earnings_calendar",
    "get_earnings_quality_score",
    # Trading
    "get_candlestick_data",
    "get_stock_splits",
    "get_technical_indicators",
    # Other
    "get_company_dividends",
    "get_company_price_metrics",
    "get_sector_metrics",
    "get_ipo_calendar",
    "get_historical_mcap",
    "get_insider_transactions",
    "get_company_filings",
    "get_historical_employee_count",
]
