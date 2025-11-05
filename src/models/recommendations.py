from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class RecommendationTrend(SQLModel, table=True):
    """Analyst recommendation trends over time.

    API Response fields: buy, hold, period, sell, strongBuy, strongSell, symbol
    """

    __tablename__ = "recommendation_trends"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    period: str = Field(index=True, max_length=20)  # e.g., '2024-01-01'

    strongBuy: Optional[int] = Field(default=None)
    buy: Optional[int] = Field(default=None)
    hold: Optional[int] = Field(default=None)
    sell: Optional[int] = Field(default=None)
    strongSell: Optional[int] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class UpgradeDowngrade(SQLModel, table=True):
    """Analyst upgrade/downgrade rating changes.

    API Response fields: symbol, gradeTime, company, fromGrade, toGrade, action
    """

    __tablename__ = "upgrade_downgrades"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    gradeTime: int = Field(index=True)  # Unix timestamp

    company: Optional[str] = Field(default=None, max_length=100)
    fromGrade: Optional[str] = Field(default=None, max_length=50)
    toGrade: Optional[str] = Field(default=None, max_length=50)
    action: Optional[str] = Field(default=None, max_length=50)  # 'up', 'down', 'init', 'main', 'reit'

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class PriceTarget(SQLModel, table=True):
    """Analyst price targets.

    API Response fields: symbol, targetHigh, targetLow, targetMean, targetMedian, lastUpdated
    """

    __tablename__ = "price_targets"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10, unique=True)

    targetHigh: Optional[float] = Field(default=None)
    targetLow: Optional[float] = Field(default=None)
    targetMean: Optional[float] = Field(default=None)
    targetMedian: Optional[float] = Field(default=None)

    lastUpdated: Optional[str] = Field(default=None, max_length=20)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
