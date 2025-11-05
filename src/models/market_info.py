from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class MarketStatus(SQLModel, table=True):
    """Market trading status.

    API Response fields: exchange, holiday, isOpen, session, timezone
    """

    __tablename__ = "market_status"

    id: Optional[int] = Field(default=None, primary_key=True)
    exchange: str = Field(index=True, max_length=50)
    checked_at: dt = Field(default_factory=lambda: dt.now(timezone.utc), index=True)

    isOpen: bool = Field(default=False)
    session: Optional[str] = Field(default=None, max_length=50)  # 'pre-market', 'regular', 'after-hours', 'closed'

    timezone: Optional[str] = Field(default=None, max_length=50)
    holiday: Optional[str] = Field(default=None, max_length=100)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class MarketHoliday(SQLModel, table=True):
    """Market holidays schedule.

    API Response fields: exchange, data (array with eventName, atDate, tradingDate)
    """

    __tablename__ = "market_holidays"

    id: Optional[int] = Field(default=None, primary_key=True)
    exchange: str = Field(index=True, max_length=50)
    atDate: str = Field(index=True, max_length=20)  # Holiday date
    tradingDate: Optional[str] = Field(default=None, max_length=20)
    eventName: Optional[str] = Field(default=None, max_length=100)

    year: Optional[int] = Field(default=None, index=True)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class SectorMetrics(SQLModel, table=True):
    """Market sector performance metrics.

    API Response fields: region, sector, and various performance metrics
    """

    __tablename__ = "sector_metrics"

    id: Optional[int] = Field(default=None, primary_key=True)
    region: str = Field(index=True, max_length=10)  # e.g., 'US'
    sector: str = Field(index=True, max_length=100)
    date: str = Field(index=True, max_length=20)

    # Performance metrics (camelCase as per API)
    performance1d: Optional[float] = Field(default=None, alias="1d")
    performance5d: Optional[float] = Field(default=None, alias="5d")
    performance1m: Optional[float] = Field(default=None, alias="1m")
    performance3m: Optional[float] = Field(default=None, alias="3m")
    performance6m: Optional[float] = Field(default=None, alias="6m")
    performanceYtd: Optional[float] = Field(default=None, alias="ytd")
    performance1y: Optional[float] = Field(default=None, alias="1y")

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
