from typing import Optional
from sqlmodel import SQLModel, Field


class EarningsData(SQLModel, table=True):
    """Earnings Data - /stock/earnings"""
    __tablename__ = "earnings_data"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    actual: Optional[float] = None
    estimate: Optional[float] = None
    surprise: Optional[float] = None
    surprise_percent: Optional[float] = Field(default=None, alias="surprisePercent")
    quarter: Optional[int] = None
    year: Optional[int] = None


class EarningsCalendar(SQLModel, table=True):
    """Earnings Calendar - /calendar/earnings"""
    __tablename__ = "earnings_calendar"

    symbol: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)

    eps_actual: Optional[float] = Field(default=None, alias="epsActual")
    eps_estimate: Optional[float] = Field(default=None, alias="epsEstimate")
    hour: Optional[str] = None
    quarter: Optional[int] = None
    revenue_actual: Optional[float] = Field(default=None, alias="revenueActual")
    revenue_estimate: Optional[float] = Field(default=None, alias="revenueEstimate")
    year: Optional[int] = None
