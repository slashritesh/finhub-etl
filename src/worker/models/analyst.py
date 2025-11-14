from typing import Optional
from sqlmodel import SQLModel, Field


class AnalystRecommendation(SQLModel, table=True):
    """Analyst Recommendations - /stock/recommendation"""
    __tablename__ = "recommendations_trends"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    buy: Optional[int] = None
    hold: Optional[int] = None
    sell: Optional[int] = None
    strong_buy: Optional[int] = Field(default=None, alias="strongBuy")
    strong_sell: Optional[int] = Field(default=None, alias="strongSell")


class PriceTarget(SQLModel, table=True):
    """Price Target - /stock/price-target"""
    __tablename__ = "price_targets"

    # Primary key fields
    symbol: str = Field(primary_key=True, index=True)
    last_updated: str = Field(primary_key=True, alias="lastUpdated")

    # Data fields
    number_analysts: Optional[int] = Field(default=None, alias="numberAnalysts")
    target_high: Optional[float] = Field(default=None, alias="targetHigh")
    target_low: Optional[float] = Field(default=None, alias="targetLow")
    target_mean: Optional[float] = Field(default=None, alias="targetMean")
    target_median: Optional[float] = Field(default=None, alias="targetMedian")


class UpgradeDowngrade(SQLModel, table=True):
    """Analyst Upgrades/Downgrades - /stock/upgrade-downgrade"""
    __tablename__ = "upgrade_downgrades"

    symbol: str = Field(primary_key=True, index=True)
    grade_time: int = Field(primary_key=True, alias="gradeTime")
    company: str = Field(primary_key=True)

    from_grade: Optional[str] = Field(default=None, alias="fromGrade")
    to_grade: Optional[str] = Field(default=None, alias="toGrade")
    action: Optional[str] = None
