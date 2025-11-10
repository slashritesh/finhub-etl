from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Text


class CompanyNews(SQLModel, table=True):
    """Company news articles.

    API Response fields: category, datetime, headline, id, image, related, source, summary, url
    """

    __tablename__ = "company_news"

    db_id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    category: Optional[str] = Field(default=None, max_length=100)
    datetime: int = Field(index=True)  # Unix timestamp
    headline: str
    id: Optional[int] = Field(default=None, unique=True)
    image: Optional[str] = Field(default=None, max_length=500)
    related: Optional[str] = Field(default=None, max_length=500)  # Comma-separated symbols
    source: Optional[str] = Field(default=None, max_length=100)
    summary: Optional[str] = Field(default=None, sa_column=Column(Text))
    url: Optional[str] = Field(default=None, max_length=500)
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class GeneralNews(SQLModel, table=True):
    """General market news.

    API Response fields: category, datetime, headline, id, image, related, source, summary, url
    """

    __tablename__ = "general_news"

    db_id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(index=True, max_length=100)
    datetime: int = Field(index=True)  # Unix timestamp
    headline: str
    id: Optional[int] = Field(default=None, unique=True)
    image: Optional[str] = Field(default=None, max_length=500)
    related: Optional[str] = Field(default=None, max_length=500)  # Comma-separated symbols
    source: Optional[str] = Field(default=None, max_length=100)
    summary: Optional[str] = Field(default=None, sa_column=Column(Text))
    url: Optional[str] = Field(default=None, max_length=500)
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class PressRelease(SQLModel, table=True):
    """Company press releases.

    API Response fields: datetime, headline, id, url
    """

    __tablename__ = "press_releases"

    db_id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    datetime: int = Field(index=True)  # Unix timestamp
    headline: str
    id: Optional[str] = Field(default=None, max_length=100, unique=True)
    url: Optional[str] = Field(default=None, max_length=500)
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
