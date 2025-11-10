from .finhub import api_client


# ========================================
# 🧠 Search & General Info
# ========================================

async def search_symbols(query):
    """Search for stock symbols.

    Args:
        query (str): Search query string

    Returns:
        dict: Search results with matching symbols
    """
    return await api_client.get("/search", params={"q": query})


async def get_stock_symbols(exchange):
    """Get all stock symbols for a given exchange.

    Args:
        exchange (str): Exchange code (e.g., 'US', 'TO', 'L')

    Returns:
        list: List of stock symbols on the exchange
    """
    return await api_client.get("/stock/symbol", params={"exchange": exchange})


# ========================================
# 🏢 Company Data
# ========================================

async def get_company_profile(symbol):
    """Get company profile (v2).

    Args:
        symbol (str): Stock symbol (e.g., 'AAPL')

    Returns:
        dict: Company profile data
    """
    return await api_client.get("/stock/profile2", params={"symbol": symbol})


async def get_executives(symbol):
    """Get company executives.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Company executives information
    """
    return await api_client.get("/stock/executive", params={"symbol": symbol})


async def get_peers(symbol):
    """Get peer companies.

    Args:
        symbol (str): Stock symbol

    Returns:
        list: List of peer company symbols
    """
    return await api_client.get("/stock/peers", params={"symbol": symbol})


# ========================================
# 💵 Quotes & Market Data
# ========================================

async def get_quote(symbol):
    """Get real-time stock quote.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Real-time quote data
    """
    return await api_client.get("/quote", params={"symbol": symbol})


async def get_order_book(symbol):
    """Get live order book data.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Order book data with bids and asks
    """
    return await api_client.get("/stock/bidask", params={"symbol": symbol})


async def get_stock_candles(symbol, resolution, from_timestamp, to_timestamp):
    """Get historical candlestick data.

    Args:
        symbol (str): Stock symbol
        resolution (str): Candle resolution ('1', '5', '15', '30', '60', 'D', 'W', 'M')
        from_timestamp (int): Unix timestamp for start date
        to_timestamp (int): Unix timestamp for end date

    Returns:
        dict: OHLCV candlestick data
    """
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": from_timestamp,
        "to": to_timestamp
    }
    return await api_client.get("/stock/candle", params=params)


# ========================================
# 📰 News & Press
# ========================================

async def get_company_news(symbol, from_date, to_date):
    """Get recent company news.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: List of news articles
    """
    params = {"symbol": symbol, "from": from_date, "to": to_date}
    return await api_client.get("/company-news", params=params)


async def get_general_news(category='general', min_id=0):
    """Get general market news.

    Args:
        category (str): News category (default: 'general')
        min_id (int): Minimum news ID for pagination

    Returns:
        list: List of general news articles
    """
    params = {"category": category, "minId": min_id}
    return await api_client.get("/news", params=params)


async def get_press_releases(symbol, from_date=None, to_date=None):
    """Get press releases for a company.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Press releases data
    """
    params = {"symbol": symbol}
    if from_date and to_date:
        params["from"] = from_date
        params["to"] = to_date
    return await api_client.get("/press-releases", params=params)


# ========================================
# 💰 Financials
# ========================================

async def get_basic_financials(symbol, metric='all'):
    """Get basic financial metrics.

    Args:
        symbol (str): Stock symbol
        metric (str): Metric type (default: 'all')

    Returns:
        dict: Basic financial metrics and ratios
    """
    params = {"symbol": symbol, "metric": metric}
    return await api_client.get("/stock/metric", params=params)


async def get_financials_as_reported(symbol, freq='annual'):
    """Get financials as reported (annual/quarterly).

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Financial reports as filed
    """
    params = {"symbol": symbol, "freq": freq}
    return await api_client.get("/stock/financials-reported", params=params)


async def get_standardized_financials(symbol, statement, freq='annual'):
    """Get standardized financial statements.

    Args:
        symbol (str): Stock symbol
        statement (str): Statement type ('income', 'balance', 'cash')
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Standardized financial statements
    """
    params = {"symbol": symbol, "statement": statement, "freq": freq}
    return await api_client.get("/stock/financials", params=params)


# ========================================
# 📈 Estimates & Earnings
# ========================================

async def get_revenue_estimates(symbol, freq='annual'):
    """Get revenue estimates.

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: Revenue estimates data
    """
    params = {"symbol": symbol, "freq": freq}
    return await api_client.get("/stock/revenue-estimate", params=params)


async def get_eps_estimates(symbol, freq='annual'):
    """Get EPS estimates.

    Args:
        symbol (str): Stock symbol
        freq (str): Frequency ('annual' or 'quarterly')

    Returns:
        dict: EPS estimates data
    """
    params = {"symbol": symbol, "freq": freq}
    return await api_client.get("/stock/eps-estimate", params=params)


async def get_earnings_calendar(from_date, to_date, symbol=None, international=False):
    """Get upcoming earnings calendar.

    Args:
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)
        symbol (str, optional): Filter by symbol
        international (bool): Include international symbols

    Returns:
        dict: Earnings calendar data
    """
    params = {"from": from_date, "to": to_date, "international": international}
    if symbol:
        params["symbol"] = symbol
    return await api_client.get("/calendar/earnings", params=params)


async def get_historical_earnings(symbol, limit=None):
    """Get past earnings data.

    Args:
        symbol (str): Stock symbol
        limit (int, optional): Limit number of results

    Returns:
        list: Historical earnings data
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    return await api_client.get("/stock/earnings", params=params)


# ========================================
# 📊 Recommendations & Ratings
# ========================================

async def get_recommendation_trends(symbol):
    """Get analyst recommendation trends.

    Args:
        symbol (str): Stock symbol

    Returns:
        list: Recommendation trends over time
    """
    return await api_client.get("/stock/recommendation", params={"symbol": symbol})


async def get_upgrade_downgrades(symbol, from_date=None, to_date=None):
    """Get upgrade/downgrade rating changes.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        list: Rating change history
    """
    params = {"symbol": symbol}
    if from_date and to_date:
        params["from"] = from_date
        params["to"] = to_date
    return await api_client.get("/stock/upgrade-downgrade", params=params)


async def get_price_target(symbol):
    """Get price targets.

    Args:
        symbol (str): Stock symbol

    Returns:
        dict: Analyst price target data
    """
    return await api_client.get("/stock/price-target", params={"symbol": symbol})


# ========================================
# 🧾 Filings, Splits, Dividends
# ========================================

async def get_dividends(symbol, from_date, to_date):
    """Get dividend data.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: Dividend history
    """
    params = {"symbol": symbol, "from": from_date, "to": to_date}
    return await api_client.get("/stock/dividend", params=params)


async def get_splits(symbol, from_date, to_date):
    """Get stock split history.

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        list: Stock split history
    """
    params = {"symbol": symbol, "from": from_date, "to": to_date}
    return await api_client.get("/stock/split", params=params)


async def get_filings(symbol, from_date=None, to_date=None, form=None):
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
        params['from'] = from_date
    if to_date:
        params['to'] = to_date
    if form:
        params['form'] = form
    return await api_client.get("/stock/filings", params=params)


# ========================================
# 👥 Insider & Institutional
# ========================================

async def get_insider_transactions(symbol, from_date=None, to_date=None):
    """Get insider transactions.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Insider transaction data
    """
    params = {"symbol": symbol}
    if from_date and to_date:
        params["from"] = from_date
        params["to"] = to_date
    return await api_client.get("/stock/insider-transactions", params=params)


async def get_institutional_ownership(symbol, from_date=None, to_date=None):
    """Get institutional ownership data.

    Args:
        symbol (str): Stock symbol
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Institutional ownership data
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    return await api_client.get("/institutional/ownership", params=params)


async def get_fund_ownership(symbol, limit=10):
    """Get fund ownership data.

    Args:
        symbol (str): Stock symbol
        limit (int): Limit number of results (default: 10)

    Returns:
        dict: Fund ownership data
    """
    params = {"symbol": symbol, "limit": limit}
    return await api_client.get("/stock/fund-ownership", params=params)


async def get_institutional_profile(cik):
    """Get institutional investor profile.

    Args:
        cik (str): CIK number of the institution

    Returns:
        dict: Institutional profile data
    """
    return await api_client.get("/institutional/profile", params={"cik": cik})


async def get_institutional_portfolio(cik, from_date=None, to_date=None):
    """Get institutional portfolio data.

    Args:
        cik (str): CIK number of the institution
        from_date (str, optional): Start date (YYYY-MM-DD)
        to_date (str, optional): End date (YYYY-MM-DD)

    Returns:
        dict: Portfolio holdings data
    """
    params = {"cik": cik}
    if from_date and to_date:
        params["from"] = from_date
        params["to"] = to_date
    return await api_client.get("/institutional/portfolio", params=params)


async def get_institutional_ownership_history(symbol, from_date, to_date):
    """Get historical institutional ownership data (alias for get_institutional_ownership).

    Args:
        symbol (str): Stock symbol
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        dict: Historical ownership data
    """
    return await get_institutional_ownership(symbol, from_date, to_date)


# ========================================
# 🗓️ Calendar & IPOs
# ========================================

async def get_ipo_calendar(from_date, to_date):
    """Get upcoming IPO calendar.

    Args:
        from_date (str): Start date (YYYY-MM-DD)
        to_date (str): End date (YYYY-MM-DD)

    Returns:
        dict: IPO calendar data
    """
    params = {"from": from_date, "to": to_date}
    return await api_client.get("/calendar/ipo", params=params)


# ========================================
# 🧭 Market Info
# ========================================

async def get_market_status(exchange):
    """Get market status.

    Args:
        exchange (str): Exchange code (e.g., 'US')

    Returns:
        dict: Current market status
    """
    return await api_client.get("/stock/market-status", params={"exchange": exchange})


async def get_market_holidays(exchange):
    """Get market holiday list.

    Args:
        exchange (str): Exchange code (e.g., 'US')

    Returns:
        dict: Market holidays
    """
    return await api_client.get("/stock/market-holiday", params={"exchange": exchange})


# ========================================
# 🧩 Sector Data
# ========================================

async def get_sector_metrics(region='US'):
    """Get metrics for various market sectors.

    Args:
        region (str): Region code (default: 'US')

    Returns:
        dict: Sector performance metrics
    """
    return await api_client.get("/sector/metrics", params={"region": region})
