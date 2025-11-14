from typing import Optional
from sqlmodel import SQLModel, Field


class EarningsQualityScore(SQLModel, table=True):
    """Earnings Quality Score - /stock/earnings-quality-score"""
    __tablename__ = "earnings_quality_scores"

    # Composite Primary Key
    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)
    
    # The 'freq' is now part of the primary key to ensure uniqueness
    # for annual vs. quarterly scores for the same period.
    freq: str = Field(primary_key=True)

    # Data Field
    score: Optional[float] = None