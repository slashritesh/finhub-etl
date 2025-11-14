from typing import Optional
from sqlmodel import SQLModel, Field


class TechnicalIndicator(SQLModel, table=True):
    """Technical Indicators - /indicator"""
    __tablename__ = "technical_indicators"

    symbol: str = Field(primary_key=True, index=True)
    timestamp: int = Field(primary_key=True, alias="t")
    indicator: str = Field(primary_key=True)

    value: Optional[float] = None
    signal: Optional[str] = None
