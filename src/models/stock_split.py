from typing import Optional
from sqlmodel import SQLModel, Field


class StockSplit(SQLModel, table=True):
    """Stock Split Data - /stock/split"""
    __tablename__ = "stock_splits"

    symbol: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)

    from_factor: Optional[float] = Field(default=None, alias="fromFactor")
    to_factor: Optional[float] = Field(default=None, alias="toFactor")
