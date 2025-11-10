from typing import Optional
from sqlmodel import SQLModel, Field


class HistoricalMarketCap(SQLModel, table=True):
    """Historical Market Cap - /stock/historical-market-cap"""
    __tablename__ = "historical_market_cap"

    symbol: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)  # YYYY-MM-DD format

    market_cap: Optional[float] = Field(default=None, alias="marketCap")
