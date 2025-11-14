from typing import Optional
from sqlmodel import SQLModel, Field


class RealtimeQuote(SQLModel, table=True):
    """Real-Time Quote - /quote"""
    __tablename__ = "realtime_quotes"

    symbol: str = Field(primary_key=True)
    timestamp: int = Field(primary_key=True, alias="t")

    current_price: Optional[float] = Field(default=None, alias="c")
    change: Optional[float] = Field(default=None, alias="d")
    percent_change: Optional[float] = Field(default=None, alias="dp")
    high: Optional[float] = Field(default=None, alias="h")
    low: Optional[float] = Field(default=None, alias="l")
    open_price: Optional[float] = Field(default=None, alias="o")
    previous_close: Optional[float] = Field(default=None, alias="pc")
