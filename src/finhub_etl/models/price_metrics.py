from typing import Optional
from sqlmodel import SQLModel, Field


class PriceMetrics(SQLModel, table=True):
    """Price Metrics - /stock/price-metric"""
    __tablename__ = "price_metrics"

    symbol: str = Field(primary_key=True)

    # 52 Week Metrics
    fifty_two_week_high: Optional[float] = Field(default=None, alias="52WeekHigh")
    fifty_two_week_high_date: Optional[str] = Field(default=None, alias="52WeekHighDate")
    fifty_two_week_low: Optional[float] = Field(default=None, alias="52WeekLow")
    fifty_two_week_low_date: Optional[str] = Field(default=None, alias="52WeekLowDate")

    # Moving Averages and Volume
    one_hundred_day_ema: Optional[float] = Field(default=None, alias="100DayEMA")
    one_hundred_day_sma: Optional[float] = Field(default=None, alias="100DaySMA")
    ten_day_average_trading_volume: Optional[float] = Field(default=None, alias="10DayAverageTradingVolume")
    ten_day_ema: Optional[float] = Field(default=None, alias="10DayEMA")
    ten_day_sma: Optional[float] = Field(default=None, alias="10DaySMA")
    fifty_day_ema: Optional[float] = Field(default=None, alias="50DayEMA")
    fifty_day_sma: Optional[float] = Field(default=None, alias="50DaySMA")
    five_day_ema: Optional[float] = Field(default=None, alias="5DayEMA")
    
    # Other Metrics
    fourteen_day_rsi: Optional[float] = Field(default=None, alias="14DayRSI")
    one_month_high: Optional[float] = Field(default=None, alias="1MonthHigh")
    one_month_high_date: Optional[str] = Field(default=None, alias="1MonthHighDate")
    ytd_price_return: Optional[float] = Field(default=None, alias="ytdPriceReturn") 
