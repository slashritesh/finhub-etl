from typing import Optional
from sqlmodel import SQLModel, Field


class BasicFinancials(SQLModel, table=True):
    """Basic Financials - /stock/metric"""
    __tablename__ = "basic_financials"
    __table_args__ = {"extend_existing": True}

    # Composite Primary Key
    symbol: str = Field(primary_key=True)
    metric_type: str = Field(primary_key=True, alias="metricType")

    # All metrics from the 'metric' object
    ten_day_avg_trading_volume: Optional[float] = Field(default=None, alias="10DayAverageTradingVolume")
    fifty_two_week_high: Optional[float] = Field(default=None, alias="52WeekHigh")
    fifty_two_week_low: Optional[float] = Field(default=None, alias="52WeekLow")
    fifty_two_week_low_date: Optional[str] = Field(default=None, alias="52WeekLowDate")
    fifty_two_week_price_return_daily: Optional[float] = Field(default=None, alias="52WeekPriceReturnDaily")
    beta: Optional[float] = Field(default=None, alias="beta")

    market_capitalization: Optional[float] = Field(default=None, alias="marketCapitalization")

class CompanyFinancials(SQLModel, table=True):
    """Company Financials - /stock/financials"""
    __tablename__ = "company_financials"

    # Composite Primary Key
    symbol: str = Field(primary_key=True, max_length=20, index=True)
    statement_type: str = Field(primary_key=True, max_length=50) # Alias removed, handler provides correct key
    period: str = Field(primary_key=True, max_length=20)
    frequency: str = Field(primary_key=True, max_length=10)

    # Financial data - all are Optional because a row will only contain data for one statement type
    revenue: Optional[float] = None
    net_income: Optional[float] = Field(default=None, alias="netIncome")
    total_assets: Optional[float] = Field(default=None, alias="totalAssets")
    total_liabilities: Optional[float] = Field(default=None, alias="totalLiabilities")
    # This field is not in the income statement/balance sheet response, but is here for cash flow
    cash_flow: Optional[float] = None

class ReportedFinancials(SQLModel, table=True):
    """Reported Financials - /stock/financials-reported"""
    __tablename__ = "reported_financials"

    symbol: str = Field(primary_key=True, index=True)
    cik: str = Field(primary_key=True)
    access_number: str = Field(primary_key=True, alias="accessNumber")

    year: Optional[int] = None
    quarter: Optional[int] = None
    form: Optional[str] = None
    start_date: Optional[str] = Field(default=None, alias="startDate")
    end_date: Optional[str] = Field(default=None, alias="endDate")
    filed_date: Optional[str] = Field(default=None, alias="filedDate")
    accepted_date: Optional[str] = Field(default=None, alias="acceptedDate")
