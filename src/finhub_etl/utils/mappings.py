"""
Mappings between Finnhub API handlers and SQLModel classes.
Used for testing and dynamic ETL operations.
"""

from finhub_etl.models import (
    StockSymbol,
    CompanyProfile,
    CompanyProfile2,
    CompanyPeer,
    CompanyNews,
    GeneralNews,
    PressRelease,
    CompanyOwnership,
    FundOwnership,
    InstitutionalOwnership,
    InstitutionalProfile,
    InstitutionalPortfolio,
    BasicFinancials,
    CompanyFinancials,
    ReportedFinancials,
    Dividend,
    PriceMetrics,
    SectorMetrics,
    IpoCalendar,
    HistoricalMarketCap,
    MarketStatus,
    MarketHoliday,
    CompanyExecutive,
    InsiderTransaction,
    CompanyFiling,
    HistoricalEmployeeCount,
    AnalystRecommendation,
    PriceTarget,
    UpgradeDowngrade,
    RevenueEstimate,
    EpsEstimate,
    EbitdaEstimate,
    EbitEstimate,
    EarningsData,
    EarningsCalendar,
    RealtimeQuote,
    CandlestickData,
    StockSplit,
    TechnicalIndicator,
    EarningsQualityScore,
)

from finhub_etl.config.handlers import (
    analyst,
    company,
    earnings,
    financials,
    market,
    news,
    ownership,
    trading,
)

HANDLER_MODEL_DICT = {
    # Analyst Handlers
    "recommendation_trends": {
        "handler": analyst.get_recommendation_trends,
        "model": AnalystRecommendation,
        "endpoint": "/stock/recommendation"
    },
    "price_target": {
        "handler": analyst.get_price_target,
        "model": PriceTarget,
        "endpoint": "/stock/price-target"
    },
    "upgrade_downgrade": {
        "handler": analyst.get_upgrade_downgrade,
        "model": UpgradeDowngrade,
        "endpoint": "/stock/upgrade-downgrade"
    },
    "revenue_estimate": {
        "handler": analyst.get_revenue_estimate,
        "model": RevenueEstimate,
        "endpoint": "/stock/revenue-estimate"
    },
    "eps_estimate": {
        "handler": analyst.get_eps_estimate,
        "model": EpsEstimate,
        "endpoint": "/stock/eps-estimate"
    },
    "ebitda_estimate": {
        "handler": analyst.get_ebitda_estimate,
        "model": EbitdaEstimate,
        "endpoint": "/stock/ebitda-estimate"
    },
    "ebit_estimate": {
        "handler": analyst.get_ebit_estimate,
        "model": EbitEstimate,
        "endpoint": "/stock/ebit-estimate"
    },

    # Company Handlers
    "company_profile": {
        "handler": company.get_company_profile,
        "model": CompanyProfile,
        "endpoint": "/stock/profile"
    },
    "company_profile2": {
        "handler": company.get_company_profile2,
        "model": CompanyProfile2,
        "endpoint": "/stock/profile2"
    },
    "company_peers": {
        "handler": company.get_company_peers,
        "model": CompanyPeer,
        "endpoint": "/stock/peers"
    },
    "company_executive": {
        "handler": company.get_executive,
        "model": CompanyExecutive,
        "endpoint": "/stock/executive"
    },
    "historical_employee_count": {
        "handler": company.get_historical_employee_count,
        "model": HistoricalEmployeeCount,
        "endpoint": "/stock/historical-employee-count"
    },
    "company_filing": {
        "handler": company.get_filings,
        "model": CompanyFiling,
        "endpoint": "/stock/filings"
    },
    "price_metrics": {
        "handler": company.get_price_metrics,
        "model": PriceMetrics,
        "endpoint": "/stock/price-metric"
    },
    "historical_market_cap": {
        "handler": company.get_historical_market_cap,
        "model": HistoricalMarketCap,
        "endpoint": "/stock/historical-market-cap"
    },

    # Earnings Handlers
    "earnings_data": {
        "handler": earnings.get_earnings,
        "model": EarningsData,
        "endpoint": "/stock/earnings"
    },
    "earnings_calendar": {
        "handler": earnings.get_earnings_calendar,
        "model": EarningsCalendar,
        "endpoint": "/calendar/earnings"
    },

    # Financials Handlers
    "basic_financials": {
        "handler": financials.get_basic_financials,
        "model": BasicFinancials,
        "endpoint": "/stock/metric"
    },
    "company_financials": {
        "handler": financials.get_financials,
        "model": CompanyFinancials,
        "endpoint": "/stock/financials"
    },
    "reported_financials": {
        "handler": financials.get_financials_reported,
        "model": ReportedFinancials,
        "endpoint": "/stock/financials-reported"
    },
    "sector_metrics": {
        "handler": financials.get_sector_metrics,
        "model": SectorMetrics,
        "endpoint": "/sector/metrics"
    },
    "earnings_quality_score": {
        "handler": financials.get_earnings_quality_score,
        "model": EarningsQualityScore,
        "endpoint": "/stock/earnings-quality-score"
    },

    # Market Handlers
    "symbol_lookup": {
        "handler": market.get_symbol_lookup,
        "model": StockSymbol,
        "endpoint": "/search"
    },
    "stock_symbols": {
        "handler": market.get_stock_symbols,
        "model": StockSymbol,
        "endpoint": "/stock/symbol"
    },
    "market_status": {
        "handler": market.get_market_status,
        "model": MarketStatus,
        "endpoint": "/stock/market-status"
    },
    "market_holiday": {
        "handler": market.get_market_holiday,
        "model": MarketHoliday,
        "endpoint": "/stock/market-holiday"
    },
    "realtime_quote": {
        "handler": market.get_quote,
        "model": RealtimeQuote,
        "endpoint": "/quote"
    },
    "candlestick_data": {
        "handler": market.get_candles,
        "model": CandlestickData,
        "endpoint": "/stock/candle"
    },
    "technical_indicator": {
        "handler": market.get_technical_indicators,
        "model": TechnicalIndicator,
        "endpoint": "/indicator"
    },

    # News Handlers
    "general_news": {
        "handler": news.get_general_news,
        "model": GeneralNews,
        "endpoint": "/news"
    },
    "company_news": {
        "handler": news.get_company_news,
        "model": CompanyNews,
        "endpoint": "/company-news"
    },
    "press_release": {
        "handler": news.get_press_releases,
        "model": PressRelease,
        "endpoint": "/press-releases2"
    },

    # Ownership Handlers
    "company_ownership": {
        "handler": ownership.get_ownership,
        "model": CompanyOwnership,
        "endpoint": "/stock/ownership"
    },
    "fund_ownership": {
        "handler": ownership.get_fund_ownership,
        "model": FundOwnership,
        "endpoint": "/stock/fund-ownership"
    },
    "institutional_profile": {
        "handler": ownership.get_institutional_profile,
        "model": InstitutionalProfile,
        "endpoint": "/institutional/profile"
    },
    "institutional_portfolio": {
        "handler": ownership.get_institutional_portfolio,
        "model": InstitutionalPortfolio,
        "endpoint": "/institutional/portfolio"
    },
    "institutional_ownership": {
        "handler": ownership.get_institutional_ownership,
        "model": InstitutionalOwnership,
        "endpoint": "/institutional/ownership"
    },
    "insider_transaction": {
        "handler": ownership.get_insider_transactions,
        "model": InsiderTransaction,
        "endpoint": "/stock/insider-transactions"
    },

    # Trading Handlers
    "ipo_calendar": {
        "handler": trading.get_ipo_calendar,
        "model": IpoCalendar,
        "endpoint": "/calendar/ipo"
    },
    "dividend": {
        "handler": trading.get_dividends,
        "model": Dividend,
        "endpoint": "/stock/dividend"
    },
    "stock_split": {
        "handler": trading.get_splits,
        "model": StockSplit,
        "endpoint": "/stock/split"
    },
}

__all__ = [
    "HANDLER_MODEL_DICT"
]
