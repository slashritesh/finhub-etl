from typing import Optional
from sqlmodel import SQLModel, Field


class SectorMetrics(SQLModel, table=True):
    """Sector Metrics - /sector/metrics"""
    __tablename__ = "sector_metrics"

    sector: str = Field(primary_key=True)
    region: str = Field(primary_key=True)

    pe_ratio: Optional[float] = Field(default=None, alias="peRatio")
    pb_ratio: Optional[float] = Field(default=None, alias="pbRatio")
    dividend_yield: Optional[float] = Field(default=None, alias="dividendYield")
    roe: Optional[float] = None  # Return on Equity
    roa: Optional[float] = None  # Return on Assets
    debt_to_equity: Optional[float] = Field(default=None, alias="debtToEquity")
    market_cap: Optional[float] = Field(default=None, alias="marketCap")
