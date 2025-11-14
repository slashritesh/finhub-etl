from typing import Optional
from sqlmodel import SQLModel, Field


class GeneralNews(SQLModel, table=True):
    """General Market News - /news"""
    __tablename__ = "general_news"

    id: int = Field(primary_key=True)
    category: Optional[str] = None
    datetime: Optional[int] = None
    headline: Optional[str] = None
    image: Optional[str] = None
    related: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
