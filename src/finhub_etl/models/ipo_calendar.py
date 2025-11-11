from typing import Optional
from sqlmodel import SQLModel, Field


class IpoCalendar(SQLModel, table=True):
    """IPO Calendar - /calendar/ipo"""
    __tablename__ = "ipo_calendar"

    symbol: str = Field(primary_key=True)
    date: str = Field(primary_key=True)

    name: str
    exchange: Optional[str] = None
    number_of_shares: Optional[int] = Field(default=None, alias="numberOfShares")
    price: Optional[float] = None
    status: Optional[str] = None
    total_shares_value: Optional[float] = Field(default=None, alias="totalSharesValue")
