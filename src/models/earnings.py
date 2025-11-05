from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class RevenueEstimate(SQLModel, table=True):
    """Revenue estimates for companies.

    API Response fields: revenueAvg, revenueHigh, revenueLow, numberAnalysts, period
    """

    __tablename__ = "revenue_estimates"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    freq: str = Field(max_length=10)  # 'annual' or 'quarterly'
    period: str = Field(index=True, max_length=20)  # e.g., '2024-12-31', '2024-03-31'

    revenueAvg: Optional[float] = Field(default=None)
    revenueHigh: Optional[float] = Field(default=None)
    revenueLow: Optional[float] = Field(default=None)
    numberAnalysts: Optional[int] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class EpsEstimate(SQLModel, table=True):
    """EPS (Earnings Per Share) estimates for companies.

    API Response fields: epsAvg, epsHigh, epsLow, numberAnalysts, period
    """

    __tablename__ = "eps_estimates"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    freq: str = Field(max_length=10)  # 'annual' or 'quarterly'
    period: str = Field(index=True, max_length=20)  # e.g., '2024-12-31', '2024-03-31'

    epsAvg: Optional[float] = Field(default=None)
    epsHigh: Optional[float] = Field(default=None)
    epsLow: Optional[float] = Field(default=None)
    numberAnalysts: Optional[int] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class EarningsCalendar(SQLModel, table=True):
    """Upcoming earnings calendar.

    API Response fields: date, epsActual, epsEstimate, hour, quarter, revenueActual, revenueEstimate, symbol, year
    """

    __tablename__ = "earnings_calendar"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    date: str = Field(index=True, max_length=20)  # Earnings date
    quarter: Optional[int] = Field(default=None)
    year: Optional[int] = Field(default=None)

    epsActual: Optional[float] = Field(default=None)
    epsEstimate: Optional[float] = Field(default=None)
    revenueActual: Optional[float] = Field(default=None)
    revenueEstimate: Optional[float] = Field(default=None)

    hour: Optional[str] = Field(default=None, max_length=20)  # 'bmo', 'amc', or specific time

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class HistoricalEarnings(SQLModel, table=True):
    """Historical earnings data.

    API Response fields: actual, estimate, period, quarter, surprise, surprisePercent, symbol, year
    """

    __tablename__ = "historical_earnings"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    period: str = Field(index=True, max_length=20)  # e.g., '2023-12-31'
    quarter: Optional[int] = Field(default=None)
    year: Optional[int] = Field(default=None)

    actual: Optional[float] = Field(default=None)
    estimate: Optional[float] = Field(default=None)
    surprise: Optional[float] = Field(default=None)
    surprisePercent: Optional[float] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
