### 🧠 **Search & General Info**

| Function                    | Endpoint                            | Description                                 |
| --------------------------- | ----------------------------------- | ------------------------------------------- |
| `searchSymbols(query)`      | `/search?q={query}`                 | Search for stock symbols.                   |
| `getStockSymbols(exchange)` | `/stock/symbol?exchange={exchange}` | Get all stock symbols for a given exchange. |

---
v
### 🏢 **Company Data**

| Function                    | Endpoint                           | Description               |
| --------------------------- | ---------------------------------- | ------------------------- |
| `getCompanyProfile(symbol)` | `/stock/profile2?symbol={symbol}`  | Get company profile (v2). |
| `getExecutives(symbol)`     | `/stock/executive?symbol={symbol}` | Get company executives.   |
| `getPeers(symbol)`          | `/stock/peers?symbol={symbol}`     | Get peer companies.       |

---

### 💵 **Quotes & Market Data**

| Function                                        | Endpoint                                                                    | Description                      |
| ----------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------- |
| `getQuote(symbol)`                              | `/quote?symbol={symbol}`                                                    | Get real-time stock quote.       |
| `getOrderBook(symbol)`                          | `/stock/orderbook?symbol={symbol}&limit=25`                                 | Get live order book data.        |
| `getStockCandles(symbol, resolution, from, to)` | `/stock/candle?symbol={symbol}&resolution={resolution}&from={from}&to={to}` | Get historical candlestick data. |

---

### 📰 **News & Press**

| Function                   | Endpoint                                            | Description                       |
| -------------------------- | --------------------------------------------------- | --------------------------------- |
| `getCompanyNews(symbol)`   | `/company-news?symbol={symbol}&from={from}&to={to}` | Get recent company news.          |
| `getGeneralNews()`         | `/news?category=general`                            | Get general market news.          |
| `getPressReleases(symbol)` | `/press-releases2?symbol={symbol}`                  | Get press releases for a company. |

---

### 💰 **Financials**

| Function                                             | Endpoint                                                              | Description                                    |
| ---------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| `getBasicFinancials(symbol)`                         | `/stock/metric?symbol={symbol}&metric=all`                            | Get basic financial metrics.                   |
| `getFinancialsAsReported(symbol, freq)`              | `/stock/financials-reported?symbol={symbol}&freq={freq}`              | Get financials as reported (annual/quarterly). |
| `getStandardizedFinancials(symbol, statement, freq)` | `/stock/financials?symbol={symbol}&statement={statement}&freq={freq}` | Get standardized financial statements.         |

---

### 📈 **Estimates & Earnings**

| Function                        | Endpoint                                  | Description                     |
| ------------------------------- | ----------------------------------------- | ------------------------------- |
| `getRevenueEstimates(symbol)`   | `/stock/revenue-estimate?symbol={symbol}` | Get revenue estimates.          |
| `getEpsEstimates(symbol)`       | `/stock/eps-estimate?symbol={symbol}`     | Get EPS estimates.              |
| `getEarningsCalendar()`         | `/calendar/earnings?from={from}&to={to}`  | Get upcoming earnings calendar. |
| `getHistoricalEarnings(symbol)` | `/stock/earnings?symbol={symbol}`         | Get past earnings data.         |

---

### 📊 **Recommendations & Ratings**

| Function                          | Endpoint                                   | Description                           |
| --------------------------------- | ------------------------------------------ | ------------------------------------- |
| `getRecommendationTrends(symbol)` | `/stock/recommendation?symbol={symbol}`    | Get analyst recommendation trends.    |
| `getUpgradeDowngrades(symbol)`    | `/stock/upgrade-downgrade?symbol={symbol}` | Get upgrade/downgrade rating changes. |
| `getPriceTarget(symbol)`          | `/stock/price-target?symbol={symbol}`      | Get price targets.                    |

---

### 🧾 **Filings, Splits, Dividends**

| Function               | Endpoint                                           | Description              |
| ---------------------- | -------------------------------------------------- | ------------------------ |
| `getDividends(symbol)` | `/stock/dividend?symbol={symbol}`                  | Get dividend data.       |
| `getSplits(symbol)`    | `/stock/split?symbol={symbol}&from={from}&to={to}` | Get stock split history. |
| `getFilings(symbol)`   | `/stock/filings?symbol={symbol}`                   | Get SEC filings.         |

---

### 👥 **Insider & Institutional**

| Function                                        | Endpoint                                                                 | Description                         |
| ----------------------------------------------- | ------------------------------------------------------------------------ | ----------------------------------- |
| `getInsiderTransactions(symbol)`                | `/stock/insider-transactions?symbol={symbol}&from={from}&to={to}`        | Get insider transactions.           |
| `getInstitutionalOwnership(symbol)`             | `/stock/ownership?symbol={symbol}&limit=10`                              | Get institutional ownership data.   |
| `getFundOwnership(symbol)`                      | `/stock/fund-ownership?symbol={symbol}&limit=10`                         | Get fund ownership data.            |
| `getInstitutionalProfile(cik)`                  | `/institutional/profile?cik={cik}`                                       | Get institutional investor profile. |
| `getInstitutionalPortfolio(cik)`                | `/institutional/portfolio?cik={cik}&from={from}&to={to}`                 | Get institutional portfolio data.   |
| `getInstitutionalOwnershipHistory(cik, symbol)` | `/institutional/ownership?symbol={symbol}&cik={cik}&from={from}&to={to}` | Get historical ownership data.      |

---

### 🗓️ **Calendar & IPOs**

| Function           | Endpoint                            | Description                |
| ------------------ | ----------------------------------- | -------------------------- |
| `getIPOCalendar()` | `/calendar/ipo?from={from}&to={to}` | Get upcoming IPO calendar. |

---

### 🧭 **Market Info**

| Function                      | Endpoint                                    | Description              |
| ----------------------------- | ------------------------------------------- | ------------------------ |
| `getMarketStatus(exchange)`   | `/stock/market-status?exchange={exchange}`  | Get market status.       |
| `getMarketHolidays(exchange)` | `/stock/market-holiday?exchange={exchange}` | Get market holiday list. |

---

### 🧩 **Sector Data**

| Function             | Endpoint         | Description                             |
| -------------------- | ---------------- | --------------------------------------- |
| `getSectorMetrics()` | `/sector/metric` | Get metrics for various market sectors. |

