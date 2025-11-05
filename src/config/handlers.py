from .finhub import finnhub_client as client


# ========================================
# 🧠 Search & General Info
# ========================================

def search_symbols(query):
    """Search for stock symbols.

    Args:
        query (str): Search query string

    Returns:
        dict: Search results with matching symbols
    """
    return client.symbol_lookup(query)


def get_stock_symbols(exchange):
    """Get all stock symbols for a given exchange.

    Args:
        exchange (str): Exchange code (e.g., 'US', 'TO', 'L')

    Returns:
        list: List of stock symbols on the exchange
    """
    return client.stock_symbols(exchange)


# ========================================
# 🏢 Company Data
# ========================================

def get_company_profile(symbol):
    """Get company profile (v2).

    Args:
        symbol (str): Stock symbol (e.g., 'AAPL')

    Returns:
        dict: Company profile data
    """
    return client.company_profile2(symbol=symbol)


def get_executives(symbol):
    """Get company executives.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Company executives information
    """
    return client.company_executive(symbol)


def get_peers(symbol):
    """Get peer companies.

    Args:
        symbol (str): Stock symbol

    Returns:
        list: List of peer company symbols
    """
    return client.company_peers(symbol)


# ========================================
# 💵 Quotes & Market Data
# ========================================

def get_quote(symbol):
    """Get real-time stock quote.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Real-time quote data
    """
    return client.quote(symbol)


def get_order_book(symbol):
    """Get live order book data.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Order book data with bids and asks
    """
    return client.stock_bid_ask(symbol)


def get_stock_candles(symbol, resolution, from_timestamp, to_timestamp):
    """Get historical candlestick data.

    Args:
        symbol (str): Stock symbol
        resolution (str): Candle resolution ('1', '5', '15', '30', '60', 'D', 'W', 'M')
        from_timestamp (int): Unix timestamp for start date
        to_timestamp (int): Unix timestamp for end date

    Returns:
        dict: OHLCV candlestick data
    """
    return client.stock_candles(symbol, resolution, from_timestamp, to_timestamp)


# ========================================
# 📰 News & Press
# ========================================

def get_company_news(symbol, from_date, to_date):
    """Get recent company news.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: List of news articles
    """
    return client.company_news(symbol, _from=from_date, to=to_date)


def get_general_news(category='general', min_id=0):
    """Get general market news.

    Args:
        category (str): News category (default: 'general')
        min_id (int): Minimum news ID for pagination

    Returns:
        list: List of general news articles
    """
    return client.general_news(category, min_id=min_id)


def get_press_releases(symbol, from_date=None, to_date=None):
    """Get press releases for a company.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Press releases data
    """
    if from_date and to_date:
        return client.press_releases(symbol, _from=from_date, to=to_date)
    return client.press_releases(symbol)


# ========================================
# 💰 Financials
# ========================================

def get_basic_financials(symbol, metric='all'):
    """Get basic financial metrics.

    Args:
        symbol (str): Stock symbol
        metric (str): Metric type (default: 'all')

    Returns:
        dict: Basic financial metrics and ratios
    """
    return client.company_basic_financials(symbol, metric)


def get_financials_as_reported(symbol, freq='annual'):
    """Get financials as reported (annual/quarterly).

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Financial reports as filed
    """
    return client.financials_reported(symbol=symbol, freq=freq)


def get_standardized_financials(symbol, statement, freq='annual'):
    """Get standardized financial statements.

    Args:
        symbol (str): Stock symbol
        statement (str): Statement type ('income', 'balance', 'cash')
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Standardized financial statements
    """
    return client.financials(symbol, statement, freq)


# ========================================
# 📈 Estimates & Earnings
# ========================================

def get_revenue_estimates(symbol, freq='annual'):
    """Get revenue estimates.

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Revenue estimates data
    """
    return client.company_revenue_estimates(symbol, freq=freq)


def get_eps_estimates(symbol, freq='annual'):
    """Get EPS estimates.

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: EPS estimates data
    """
    return client.company_eps_estimates(symbol, freq=freq)


def get_earnings_calendar(from_date, to_date, symbol=None, international=False):
    """Get upcoming earnings calendar.

    Args:
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)
        symbol (str, optional): Filter by symbol
        international (bool): Include international symbols

    Returns:
        dict: Earnings calendar data
    """
    return client.earnings_calendar(_from=from_date, to=to_date, symbol=symbol, international=international)


def get_historical_earnings(symbol, limit=None):
    """Get past earnings data.

    Args:
        symbol (str): Stock symbol
        limit (int, optional): Limit number of results

    Returns:
        list: Historical earnings data
    """
    return client.company_earnings(symbol, limit=limit)


# ========================================
# 📊 Recommendations & Ratings
# ========================================

def get_recommendation_trends(symbol):
    """Get analyst recommendation trends.

    Args:
        symbol (str): Stock symbol

    Returns:
        list: Recommendation trends over time
    """
    return client.recommendation_trends(symbol)


def get_upgrade_downgrades(symbol, from_date=None, to_date=None):
    """Get upgrade/downgrade rating changes.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        list: Rating change history
    """
    if from_date and to_date:
        return client.upgrade_downgrade(symbol=symbol, _from=from_date, to=to_date)
    return client.upgrade_downgrade(symbol=symbol)


def get_price_target(symbol):
    """Get price targets.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Analyst price target data
    """
    return client.price_target(symbol)


# ========================================
# 🧾 Filings, Splits, Dividends
# ========================================

def get_dividends(symbol, from_date, to_date):
    """Get dividend data.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: Dividend history
    """
    return client.stock_dividends(symbol, from_date, to_date)


def get_splits(symbol, from_date, to_date):
    """Get stock split history.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: Stock split history
    """
    return client.stock_splits(symbol, from_date, to_date)


def get_filings(symbol, from_date=None, to_date=None, form=None):
    """Get SEC filings.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)
        form (str, optional): Filing form type

    Returns:
        list: SEC filings data
    """
    params = {'symbol': symbol}
    if from_date:
        params['_from'] = from_date
    if to_date:
        params['to'] = to_date
    if form:
        params['form'] = form
    return client.filings(**params)


# ========================================
# 👥 Insider & Institutional
# ========================================

def get_insider_transactions(symbol, from_date=None, to_date=None):
    """Get insider transactions.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Insider transaction data
    """
    if from_date and to_date:
        return client.stock_insider_transactions(symbol, _from=from_date, to=to_date)
    return client.stock_insider_transactions(symbol)


def get_institutional_ownership(symbol, limit=10):
    """Get institutional ownership data.

    Args:
        symbol (str): Stock symbol
        limit (int): Limit number of results (default: 10)

    Returns:
        dict: Institutional ownership data
    """
    return client.institutional_ownership(symbol, limit=limit)


def get_fund_ownership(symbol, limit=10):
    """Get fund ownership data.

    Args:
        symbol (str): Stock symbol
        limit (int): Limit number of results (default: 10)

    Returns:
        dict: Fund ownership data
    """
    return client.fund_ownership(symbol, limit=limit)


def get_institutional_profile(cik):
    """Get institutional investor profile.

    Args:
        cik (str): CIK number of the institution

    Returns:
        dict: Institutional profile data
    """
    return client.institutional_profile(cik=cik)


def get_institutional_portfolio(cik, from_date=None, to_date=None):
    """Get institutional portfolio data.

    Args:
        cik (str): CIK number of the institution
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Portfolio holdings data
    """
    if from_date and to_date:
        return client.institutional_portfolio(cik=cik, _from=from_date, to=to_date)
    return client.institutional_portfolio(cik=cik)


def get_institutional_ownership_history(symbol, cik, from_date=None, to_date=None):
    """Get historical ownership data.

    Args:
        symbol (str): Stock symbol
        cik (str): CIK number of the institution
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Historical ownership data
    """
    if from_date and to_date:
        return client.institutional_ownership(symbol=symbol, cik=cik, _from=from_date, to=to_date)
    return client.institutional_ownership(symbol=symbol, cik=cik)


# ========================================
# 🗓️ Calendar & IPOs
# ========================================

def get_ipo_calendar(from_date, to_date):
    """Get upcoming IPO calendar.

    Args:
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        dict: IPO calendar data
    """
    return client.ipo_calendar(_from=from_date, to=to_date)


# ========================================
# 🧭 Market Info
# ========================================

def get_market_status(exchange):
    """Get market status.

    Args:
        exchange (str): Exchange code (e.g., 'US')

    Returns:
        dict: Current market status
    """
    return client.market_status(exchange=exchange)


def get_market_holidays(exchange):
    """Get market holiday list.

    Args:
        exchange (str): Exchange code (e.g., 'US')

    Returns:
        dict: Market holidays
    """
    return client.market_holiday(exchange=exchange)


# ========================================
# 🧩 Sector Data
# ========================================

def get_sector_metrics(region='US'):
    """Get metrics for various market sectors.

    Args:
        region (str): Region code (default: 'US')

    Returns:
        dict: Sector performance metrics
    """
    return client.sector_metric(region)
