"""
Scheduler job functions for all Finnhub API handlers.
"""

from .analyst_jobs import (
    recommendation_trends_job,
    price_target_job,
    upgrade_downgrade_job,
    revenue_estimate_job,
    eps_estimate_job,
    ebitda_estimate_job,
    ebit_estimate_job,
)

from .company_jobs import (
    company_profile_job,
    company_profile2_job,
    company_peers_job,
    company_executive_job,
    historical_employee_count_job,
    company_filing_job,
    price_metrics_job,
    historical_market_cap_job,
)

from .earnings_jobs import (
    earnings_data_job,
    earnings_calendar_job,
)

from .financials_jobs import (
    basic_financials_job,
    company_financials_job,
    reported_financials_job,
    sector_metrics_job,
    earnings_quality_score_job,
)

from .market_jobs import (
    stock_symbols_job,
    market_status_job,
    market_holiday_job,
    realtime_quote_job,
    candlestick_data_job,
    technical_indicator_job,
)

from .news_jobs import (
    general_news_job,
    company_news_job,
    press_release_job,
)

from .ownership_jobs import (
    company_ownership_job,
    fund_ownership_job,
    institutional_profile_job,
    institutional_portfolio_job,
    institutional_ownership_job,
    insider_transaction_job,
)

from .trading_jobs import (
    ipo_calendar_job,
    dividend_job,
    stock_split_job,
)

__all__ = [
    # Analyst jobs
    "recommendation_trends_job",
    "price_target_job",
    "upgrade_downgrade_job",
    "revenue_estimate_job",
    "eps_estimate_job",
    "ebitda_estimate_job",
    "ebit_estimate_job",
    # Company jobs
    "company_profile_job",
    "company_profile2_job",
    "company_peers_job",
    "company_executive_job",
    "historical_employee_count_job",
    "company_filing_job",
    "price_metrics_job",
    "historical_market_cap_job",
    # Earnings jobs
    "earnings_data_job",
    "earnings_calendar_job",
    # Financials jobs
    "basic_financials_job",
    "company_financials_job",
    "reported_financials_job",
    "sector_metrics_job",
    "earnings_quality_score_job",
    # Market jobs
    "stock_symbols_job",
    "market_status_job",
    "market_holiday_job",
    "realtime_quote_job",
    "candlestick_data_job",
    "technical_indicator_job",
    # News jobs
    "general_news_job",
    "company_news_job",
    "press_release_job",
    # Ownership jobs
    "company_ownership_job",
    "fund_ownership_job",
    "institutional_profile_job",
    "institutional_portfolio_job",
    "institutional_ownership_job",
    "insider_transaction_job",
    # Trading jobs
    "ipo_calendar_job",
    "dividend_job",
    "stock_split_job",
]
