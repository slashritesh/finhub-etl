"""
Example Model - Minimal boilerplate for database schema
"""
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ExampleData(SQLModel, table=True):
    """Example data model - customize this for your needs"""
    __tablename__ = "example_data"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required fields
    symbol: str = Field(index=True)  # e.g., "AAPL"
    data_type: str  # e.g., "metrics", "news", etc.

    # Optional fields with snake_case (database) and camelCase (API) mapping
    value: Optional[float] = None
    description: Optional[str] = None
    source_url: Optional[str] = Field(default=None, alias="sourceUrl")

    # Timestamps
    fetched_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    data_date: Optional[str] = Field(default=None, alias="dataDate")
