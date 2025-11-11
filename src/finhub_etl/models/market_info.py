from typing import Optional
from sqlmodel import SQLModel, Field


class MarketStatus(SQLModel, table=True):
    """Market Status - /stock/market-status"""
    __tablename__ = "market_status"

    exchange: str = Field(primary_key=True)
    timezone: Optional[str] = None
    is_open: Optional[bool] = Field(default=None, alias="isOpen")
    session: Optional[str] = None
    holiday: Optional[str] = None


class MarketHoliday(SQLModel, table=True):
    """Market Holidays - /stock/market-holiday"""
    __tablename__ = "market_holidays"

    exchange: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)
    holiday_name: Optional[str] = Field(default=None, alias="holidayName")
    event: Optional[str] = None
    hours: Optional[str] = None
