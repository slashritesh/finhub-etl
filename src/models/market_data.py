from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class StockQuote(SQLModel, table=True):
    """Real-time stock quote data.

    API Response fields: c, d, dp, h, l, o, pc, t
    """

    __tablename__ = "stock_quotes"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    c: Optional[float] = Field(default=None)  # Current price
    d: Optional[float] = Field(default=None)  # Change
    dp: Optional[float] = Field(default=None)  # Percent change
    h: Optional[float] = Field(default=None)  # High price of the day
    l: Optional[float] = Field(default=None)  # Low price of the day
    o: Optional[float] = Field(default=None)  # Open price of the day
    pc: Optional[float] = Field(default=None)  # Previous close price
    t: Optional[int] = Field(default=None)  # Timestamp
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class StockCandle(SQLModel, table=True):
    """Historical candlestick data.

    API Response fields: c, h, l, o, v, t, s
    """

    __tablename__ = "stock_candles"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    resolution: str = Field(max_length=5)  # '1', '5', '15', '30', '60', 'D', 'W', 'M'
    t: int = Field(index=True)  # Timestamp
    o: float  # Open price
    h: float  # High price
    l: float  # Low price
    c: float  # Close price
    v: Optional[float] = Field(default=None)  # Volume
    s: Optional[str] = Field(default=None, max_length=20)  # Status (ok/no_data)
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class OrderBookEntry(SQLModel, table=True):
    """Order book bid/ask entry.

    API Response fields: p (price), v (volume)
    """

    __tablename__ = "order_book_entries"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    side: str = Field(max_length=4)  # 'bid' or 'ask'
    p: float  # Price
    v: float  # Volume
    timestamp: dt = Field(default_factory=lambda: dt.now(timezone.utc), index=True)
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
