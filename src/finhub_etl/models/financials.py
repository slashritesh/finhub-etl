from typing import Optional
from sqlmodel import SQLModel, Field


class BasicFinancials(SQLModel, table=True):
    """Basic Financials - /stock/metric"""
    __tablename__ = "basic_financials"

    symbol: str = Field(primary_key=True)
    metric_type: str = Field(primary_key=True, alias="metricType")

    # Common metrics (stored as JSON in reality, but here we'll store key metrics)
    ten_day_avg_trading_volume: Optional[float] = Field(default=None, alias="10DayAverageTradingVolume")
    fifty_two_week_high: Optional[float] = Field(default=None, alias="52WeekHigh")
    fifty_two_week_low: Optional[float] = Field(default=None, alias="52WeekLow")
    beta: Optional[float] = None
    market_capitalization: Optional[float] = Field(default=None, alias="marketCapitalization")
    pe_ratio: Optional[float] = Field(default=None, alias="peBasicExclExtraTTM")
    eps: Optional[float] = Field(default=None, alias="epsBasicExclExtraItemsTTM")

class CompanyFinancials(SQLModel, table=True):
    """Company Financials - /stock/financials"""
    __tablename__ = "company_financials"

    symbol: str = Field(primary_key=True, max_length=20, index=True)
    statement_type: str = Field(primary_key=True, max_length=50, alias="statementType")  # income, balance_sheet, cash_flow
    period: str = Field(primary_key=True, max_length=20)  # YYYY-MM-DD or similar
    frequency: str = Field(primary_key=True, max_length=10)  # annual or quarterly

    # Financial data
    revenue: Optional[float] = None
    net_income: Optional[float] = Field(default=None, alias="netIncome")
    total_assets: Optional[float] = Field(default=None, alias="totalAssets")
    total_liabilities: Optional[float] = Field(default=None, alias="totalLiabilities")
    cash_flow: Optional[float] = Field(default=None, alias="cashFlow")

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
