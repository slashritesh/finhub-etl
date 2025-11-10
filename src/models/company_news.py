from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyNews(SQLModel, table=True):
    """Company News - /company-news"""
    __tablename__ = "company_news"

    # Composite primary key: symbol + datetime + id
    symbol: str = Field(primary_key=True, index=True)
    datetime: int = Field(primary_key=True)  # Unix timestamp
    id: int = Field(primary_key=True)

    category: Optional[str] = None
    headline: Optional[str] = None
    image: Optional[str] = None
    related: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
