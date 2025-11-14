from typing import Optional
from sqlmodel import SQLModel, Field


class CandlestickData(SQLModel, table=True):
    """Historical Candlestick Data - /stock/candle"""
    __tablename__ = "candlestick_data"

    symbol: str = Field(primary_key=True, index=True)
    timestamp: int = Field(primary_key=True, alias="t")
    datetime: str = Field(primary_key=True, alias="datetime")

    close: Optional[float] = Field(default=None, alias="c")
    high: Optional[float] = Field(default=None, alias="h")
    low: Optional[float] = Field(default=None, alias="l")
    open: Optional[float] = Field(default=None, alias="o")
    volume: Optional[float] = Field(default=None, alias="v")
    status: Optional[str] = Field(default=None, alias="s")
