# Finnhub API Documentation

## Overview

Finnhub provides a comprehensive REST API for accessing realtime stock, forex, and cryptocurrency data, along with company fundamentals and economic information.

**Base URL:** `https://finnhub.io/api/v1`

**Official Documentation:** https://finnhub.io/docs/api

## Authentication

All GET requests require authentication via one of these methods:

- **URL parameter:** `token=apiKey`
- **Header:** `X-Finnhub-Token: apiKey`

API keys are available in the user dashboard after registration.

## Rate Limits

- **Plan limits:** Vary by subscription tier
- **Hard limit:** 30 API calls per second
- **Exceeded limit response:** HTTP 429 status code

## API Schema

The documentation includes extensive type definitions for data objects, organized into major categories.

---

## Market Data Endpoints

### Quote Data

Get real-time quote data for stocks, forex, and cryptocurrencies.

**Fields include:**
- Current price
- Change and percent change
- High/low prices
- Open price
- Previous close

### Candle Data

OHLCV (Open, High, Low, Close, Volume) data with timestamps.

**Supported asset types:**
- Stocks
- Crypto
- Forex
- Bonds

**Response includes:**
- Status indicators (ok/no_data)
- Timestamp arrays
- OHLCV arrays

### Tick Data

Granular trade data with conditions and venues.

**Features:**
- Large dataset support with pagination
- Trade conditions
- Trading venues
- Timestamp precision

---

## Company Data Endpoints

### Profile Information

Comprehensive company details including:
- Company name, ticker, exchange
- Sector and industry classification
- Market capitalization
- Employee count
- Financial metrics
- Logo, website, contact information

### Fundamentals

Financial metrics and ratios:
- Basic financial metrics
- Time-series financial data
- Financial statements (income statement, balance sheet, cash flow)

### Ownership Data

**Institutional Ownership:**
- Holdings details
- Portfolio changes
- Filing dates

**Fund Ownership:**
- Mutual fund holdings
- ETF holdings

**Insider Transactions:**
- Transaction details
- Insider sentiment metrics
- Filing information

---

## News & Sentiment

### Company News

Access company-related news articles.

**Data includes:**
- Headline and summary
- Source and URL
- Category
- Publication timestamps
- Related ticker mentions

### News Sentiment

Sentiment analysis for news articles.

**Metrics:**
- Bullish/bearish percentages
- Company news scores
- Sector comparisons
- Article counts

---

## Earnings Data

### Earnings Calendar

Track earnings release schedules.

**Information provided:**
- Release dates and times
- EPS estimates and actuals
- Revenue estimates and actuals
- Surprise metrics (actual vs. estimate)

### Earnings Call Transcripts

Access earnings call transcripts and recordings.

**Features:**
- Full transcript content
- Participant listings
- Audio recordings
- Timestamps

---

## Additional Data Categories

### Economic Data

- Economic calendar
- Historical economic indicators
- Country-specific data

### SEC Filings

- Filing documents
- Sentiment analysis of filings
- Filing dates and types

### Patent Information

- USPTO patent data
- Patent applications and grants
- Assignee information

### Government Data

- Government spending data
- Contract information

### Employment Data

- H-1B visa applications
- Employer information

### Investment Funds

**ETF Data:**
- Holdings
- Profile information
- Exposure data

**Mutual Fund Data:**
- Holdings
- Profile information
- Performance metrics

### Technical Analysis

- Technical indicators
- Pattern recognition
- Support and resistance levels

### Analyst Data

- Analyst recommendations
- Price targets
- Rating changes
- Consensus estimates

---

## Response Format

All responses are JSON-encoded with standard HTTP status codes.

**Common HTTP Status Codes:**
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `403 Forbidden` - Insufficient permissions
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Official SDKs

Finnhub maintains official client libraries for:

- **Python** - `finnhub-python`
- **Go**
- **JavaScript/Node.js**
- **Ruby**
- **Kotlin**
- **PHP**

### Python Example

```python
import finnhub

# Setup client
finnhub_client = finnhub.Client(api_key="YOUR_API_KEY")

# Get quote
quote = finnhub_client.quote('AAPL')

# Get company profile
profile = finnhub_client.company_profile2(symbol='AAPL')

# Get candles
candles = finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)

# Get company news
news = finnhub_client.company_news('AAPL', _from="2020-01-01", to="2020-12-31")
```

---

## Best Practices

1. **Cache responses** - Reduce API calls by caching data when appropriate
2. **Respect rate limits** - Implement exponential backoff for 429 responses
3. **Use batch endpoints** - When available, use batch endpoints to reduce call count
4. **Handle errors gracefully** - Implement proper error handling for all API calls
5. **Keep API keys secure** - Never commit API keys to version control

---

## Resources

- **Official Documentation:** https://finnhub.io/docs/api
- **API Console:** https://finnhub.io/docs/api
- **Swagger Schema:** Available for download
- **Support:** Contact via website

---

*Last Updated: 2025-11-05*
*This documentation is a summary. For complete endpoint specifications, parameter details, and request examples, consult the official Finnhub API documentation.*
