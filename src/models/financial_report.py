from sqlmodel import SQLModel, Field, Column, JSON
from typing import Optional
from datetime import datetime


class FinancialReport(SQLModel, table=True):
    """Model for storing financial reports from Finnhub API."""

    id: Optional[int] = Field(default=None, primary_key=True)

    # Report metadata
    access_number: str = Field(index=True)
    symbol: str = Field(index=True)
    cik: str = Field(index=True)
    year: int = Field(index=True)
    quarter: int  # 0 for annual, 1-4 for quarters
    form: str  # e.g., "10-K", "10-Q"

    # Dates
    start_date: datetime
    end_date: datetime
    filed_date: datetime
    accepted_date: datetime

    # Financial data stored as JSON
    # Contains: bs (balance sheet), ic (income statement), cf (cash flow)
    report_data: dict = Field(sa_column=Column(JSON))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
