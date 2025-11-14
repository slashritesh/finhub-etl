from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Text


class MatchedStock(SQLModel, table=True):
    """Matched Stock data from CSV import"""
    __tablename__ = "matched_stocks"

    # Primary key
    id: str = Field(primary_key=True, nullable=False)

    # Basic stock information
    type: Optional[str] = None
    name: Optional[str] = None
    isin: Optional[str] = Field(default=None, index=True)
    exchange: Optional[str] = Field(default=None, index=True)
    symbol: Optional[str] = Field(default=None, index=True)
    key: Optional[str] = None
    sub_industry: Optional[str] = None
    ticker: Optional[str] = None
    is_active: Optional[int] = None

    # Location and currency
    country: Optional[str] = None
    currency: Optional[str] = None

    # Price information
    last_price: Optional[float] = None
    change: Optional[float] = None
    changePercent: Optional[float] = Field(default=None, alias="changePercent")
    market_cap: Optional[float] = None

    # Description and exchange details
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    exchange_name: Optional[str] = None
    indicator: Optional[str] = None
    type_stock: Optional[str] = None

    # Timestamps
    created_at: Optional[datetime] = None
    last_action_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    # Additional fields
    exchange_currency_id: Optional[str] = None
    min_order_size: Optional[float] = None
    is_deleted: Optional[int] = None

    # Finnhub fields
    displaySymbol: Optional[str] = Field(default=None, alias="displaySymbol")
    finnhubCurrency: Optional[str] = Field(default=None, alias="finnhubCurrency")
    finnhubDescription: Optional[str] = Field(default=None, alias="finnhubDescription")
    finnhubSymbol: Optional[str] = Field(default=None, alias="finnhubSymbol", index=True)
    finnhubType: Optional[str] = Field(default=None, alias="finnhubType")
    finnhubMic: Optional[str] = Field(default=None, alias="finnhubMic")
    finnhubSheet: Optional[str] = Field(default=None, alias="finnhubSheet")

    # Match metadata
    matchedBy: Optional[str] = Field(default=None, alias="matchedBy")
