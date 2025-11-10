from typing import Optional
from sqlmodel import SQLModel, Field


class PriceMetrics(SQLModel, table=True):
    """Price Metrics - /stock/price-metric"""
    __tablename__ = "price_metrics"

    symbol: str = Field(primary_key=True)

    fifty_two_week_high: Optional[float] = Field(default=None, alias="52WeekHigh")
    fifty_two_week_low: Optional[float] = Field(default=None, alias="52WeekLow")
    fifty_two_week_price_return_daily: Optional[float] = Field(default=None, alias="52WeekPriceReturnDaily")
    ytd_price_return_daily: Optional[float] = Field(default=None, alias="ytdPriceReturnDaily")
    month_to_date_price_return_daily: Optional[float] = Field(default=None, alias="monthToDatePriceReturnDaily")
    week_to_date_price_return_daily: Optional[float] = Field(default=None, alias="weekToDatePriceReturnDaily")
    current_price: Optional[float] = Field(default=None, alias="currentPrice")
