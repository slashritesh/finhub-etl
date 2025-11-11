from typing import Optional
from sqlmodel import SQLModel, Field


class EarningsQualityScore(SQLModel, table=True):
    """Earnings Quality Score - /stock/earnings-quality-score"""
    __tablename__ = "earnings_quality_scores"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    score: Optional[float] = None
    freq: Optional[str] = None
