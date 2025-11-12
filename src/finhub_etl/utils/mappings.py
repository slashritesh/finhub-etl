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
        "endpoint": "/stock/recommendation",
        "params": {
            "symbol": "AAPL",
        },
    },
    "price_target": {
        "handler": analyst.get_price_target,
        "model": PriceTarget,
        "endpoint": "/stock/price-target",
        "params": {
            "symbol": "AAPL",
        },
    },
    "upgrade_downgrade": {
        "handler": analyst.get_upgrade_downgrade,
        "model": UpgradeDowngrade,
        "endpoint": "/stock/upgrade-downgrade",
        "params": {
            "symbol": "AAPL",
            "from_date": "",
            "to_date": "",
        },
    },
    "revenue_estimate": {
        "handler": analyst.get_revenue_estimate,
        "model": RevenueEstimate,
        "endpoint": "/stock/revenue-estimate",
        "params": {
            "symbol": "AAPL",
            "freq": "quarterly",
        },
    },
    "eps_estimate": {
        "handler": analyst.get_eps_estimate,
        "model": EpsEstimate,
        "endpoint": "/stock/eps-estimate",
        "params": {
            "symbol": "AAPL",
            "freq": "quarterly",
        },
    },
    "ebitda_estimate": {
        "handler": analyst.get_ebitda_estimate,
        "model": EbitdaEstimate,
        "endpoint": "/stock/ebitda-estimate",
        "params": {
            "symbol": "AAPL",
            "freq": "quarterly",
        },
    },
    "ebit_estimate": {
        "handler": analyst.get_ebit_estimate,
        "model": EbitEstimate,
        "endpoint": "/stock/ebit-estimate",
        "params": {
            "symbol": "AAPL",
            "freq": "quarterly",
        },
    },
    # Company Handlers
    "company_profile": {
        "handler": company.get_company_profile,
        "model": CompanyProfile,
        "endpoint": "/stock/profile",
        "params": {
            "symbol": "AAPL",
            "isin": "",
            "cusip": "",
        },
    },
    "company_profile2": {
        "handler": company.get_company_profile2,
        "model": CompanyProfile2,
        "endpoint": "/stock/profile2",
        "params": {
            "symbol": "AAPL",
            "isin": "",
            "cusip": "",
        },
    },
    "company_peers": {
        "handler": company.get_company_peers,
        "model": CompanyPeer,
        "endpoint": "/stock/peers",
        "params": {
            "symbol": "AAPL",
            "grouping": "industry",
        },
    },
    "company_executive": {
        "handler": company.get_executive,
        "model": CompanyExecutive,
        "endpoint": "/stock/executive",
        "params": {
            "symbol": "AAPL",
        },
    },
    "historical_employee_count": {
        "handler": company.get_historical_employee_count,
        "model": HistoricalEmployeeCount,
        "endpoint": "/stock/historical-employee-count",
        "params": {
            "symbol": "AAPL",
            "_from": "2020-01-01",
            "to": "2024-01-01"
        },
    },
    "company_filing": {
        "handler": company.get_filings,
        "model": CompanyFiling,
        "endpoint": "/stock/filings",
        "params": {
            "symbol": "AAPL",
            "from_date": "",
            "to_date": "",
            "form": "",
        },
    },
    "price_metrics": {
        "handler": company.get_price_metrics,
        "model": PriceMetrics,
        "endpoint": "/stock/price-metric",
        "params": {
            "symbol": "AAPL",
            "date": "",
        },
    },
    "historical_market_cap": {
        "handler": company.get_historical_market_cap,
        "model": HistoricalMarketCap,
        "endpoint": "/stock/historical-market-cap",
        "params": {
            "symbol": "AAPL",
            "from_date": "",
            "to_date": "",
        },
    },
    # Earnings Handlers
    "earnings_data": {
        "handler": earnings.get_earnings,
        "model": EarningsData,
        "endpoint": "/stock/earnings",
        "params": {
            "symbol": "AAPL",
            "limit": "",
        },
    },
    "earnings_calendar": {
        "handler": earnings.get_earnings_calendar,
        "model": EarningsCalendar,
        "endpoint": "/calendar/earnings",
        "params": {
            "from_date": "",
            "to_date": "",
            "symbol": "",
            "international": False,
        },
    },
    # Financials Handlers
    "basic_financials": {
        "handler": financials.get_basic_financials,
        "model": BasicFinancials,
        "endpoint": "/stock/metric",
        "params": {
            "symbol": "AAPL",
            "metric": "all",
        },
    },
    "company_financials": {
        "handler": financials.get_financials,
        "model": CompanyFinancials,
        "endpoint": "/stock/financials",
        "params": {
            "symbol": "AAPL",
            "statement": "bs",
            "freq": "annual",
        },
    },
    "reported_financials": {
        "handler": financials.get_financials_reported,
        "model": ReportedFinancials,
        "endpoint": "/stock/financials-reported",
        "params": {
            "symbol": "AAPL",
            "freq": "annual",
        },
    },
    "sector_metrics": {
        "handler": financials.get_sector_metrics,
        "model": SectorMetrics,
        "endpoint": "/sector/metrics",
        "params": {
            "region": "us",
        },
    },
    "earnings_quality_score": {
        "handler": financials.get_earnings_quality_score,
        "model": EarningsQualityScore,
        "endpoint": "/stock/earnings-quality-score",
        "params": {
            "symbol": "AAPL",
            "freq": "quarterly",
        },
    },
    # Market Handlers
    "symbol_lookup": {
        "handler": market.get_symbol_lookup,
        "model": StockSymbol,
        "endpoint": "/search",
        "params": {
            "query": "apple",
        },
    },
    "stock_symbols": {
        "handler": market.get_stock_symbols,
        "model": StockSymbol,
        "endpoint": "/stock/symbol",
        "params": {
            "exchange": "US",
            "mic": "",
            "security_type": "",
            "currency": "",
        },
    },
    "market_status": {
        "handler": market.get_market_status,
        "model": MarketStatus,
        "endpoint": "/stock/market-status",
        "params": {
            "exchange": "US",
        },
    },
    "market_holiday": {
        "handler": market.get_market_holiday,
        "model": MarketHoliday,
        "endpoint": "/stock/market-holiday",
        "params": {
            "exchange": "US",
        },
    },
    "realtime_quote": {
        "handler": market.get_quote,
        "model": RealtimeQuote,
        "endpoint": "/quote",
        "params": {
            "symbol": "AAPL",
        },
    },
    "candlestick_data": {
        "handler": market.get_candles,
        "model": CandlestickData,
        "endpoint": "/stock/candle",
        "params": {
            "symbol": "AAPL",
            "resolution": "D",
            "from_timestamp": 1672531200,
            "to_timestamp": 1704067200,
        },
    },
    "technical_indicator": {
        "handler": market.get_technical_indicators,
        "model": TechnicalIndicator,
        "endpoint": "/indicator",
        "params": {
            "symbol": "AAPL",
            "resolution": "D",
            "from_timestamp": 1672531200,
            "to_timestamp": 1704067200,
            "indicator": "rsi",
        },
    },
    # News Handlers
    "general_news": {
        "handler": news.get_general_news,
        "model": GeneralNews,
        "endpoint": "/news",
        "params": {
            "category": "general",
            "min_id": "",
        },
    },
    "company_news": {
        "handler": news.get_company_news,
        "model": CompanyNews,
        "endpoint": "/company-news",
        "params": {
            "symbol": "AAPL",
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
        },
    },
    "press_release": {
        "handler": news.get_press_releases,
        "model": PressRelease,
        "endpoint": "/press-releases2",
        "params": {
            "symbol": "AAPL",
            "from_date": "",
            "to_date": "",
        },
    },
    # Ownership Handlers
    "company_ownership": {
        "handler": ownership.get_ownership,
        "model": CompanyOwnership,
        "endpoint": "/stock/ownership",
        "params": {
            "symbol": "AAPL",
            "limit": "",
        },
    },
    "fund_ownership": {
        "handler": ownership.get_fund_ownership,
        "model": FundOwnership,
        "endpoint": "/stock/fund-ownership",
        "params": {
            "symbol": "AAPL",
            "limit": "",
        },
    },
    "institutional_profile": {
        "handler": ownership.get_institutional_profile,
        "model": InstitutionalProfile,
        "endpoint": "/institutional/profile",
        "params": {
            "cik": "",
            "isin": "",
        },
    },
    "institutional_portfolio": {
        "handler": ownership.get_institutional_portfolio,
        "model": InstitutionalPortfolio,
        "endpoint": "/institutional/portfolio",
        "params": {
            "cik": "0001067983",
            "from_date": "",
            "to_date": "",
        },
    },
    "institutional_ownership": {
        "handler": ownership.get_institutional_ownership,
        "model": InstitutionalOwnership,
        "endpoint": "/institutional/ownership",
        "params": {
            "symbol": "AAPL",
            "cusip": "",
            "from_date": "",
            "to_date": "",
        },
    },
    "insider_transaction": {
        "handler": ownership.get_insider_transactions,
        "model": InsiderTransaction,
        "endpoint": "/stock/insider-transactions",
        "params": {
            "symbol": "AAPL",
            "from_date": "",
            "to_date": "",
        },
    },
    # Trading Handlers
    "ipo_calendar": {
        "handler": trading.get_ipo_calendar,
        "model": IpoCalendar,
        "endpoint": "/calendar/ipo",
        "params": {
            "from_date": "2024-01-01",
            "to_date": "2024-12-31",
        },
    },
    "dividend": {
        "handler": trading.get_dividends,
        "model": Dividend,
        "endpoint": "/stock/dividend",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
    "stock_split": {
        "handler": trading.get_splits,
        "model": StockSplit,
        "endpoint": "/stock/split",
        "params": {
            "symbol": "AAPL",
            "from_date": "2020-01-01",
            "to_date": "2024-12-31",
        },
    },
}

__all__ = ["HANDLER_MODEL_DICT"]
