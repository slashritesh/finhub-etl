from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class IpoCalendar(SQLModel, table=True):
    """IPO calendar and offerings.

    API Response fields: symbol, date, exchange, name, price, numberOfShares, totalSharesValue, status
    """

    __tablename__ = "ipo_calendar"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    date: str = Field(index=True, max_length=20)  # IPO date

    name: Optional[str] = Field(default=None, max_length=200)
    exchange: Optional[str] = Field(default=None, max_length=50)

    price: Optional[float] = Field(default=None)
    numberOfShares: Optional[float] = Field(default=None)
    totalSharesValue: Optional[float] = Field(default=None)

    status: Optional[str] = Field(
        default=None, max_length=50
    )  # 'priced', 'expected', 'filed', 'withdrawn'

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
