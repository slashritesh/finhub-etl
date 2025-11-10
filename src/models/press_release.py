from typing import Optional
from sqlmodel import SQLModel, Field


class PressRelease(SQLModel, table=True):
    """Press Releases - /press-releases"""
    __tablename__ = "press_releases"

    symbol: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)  # YYYY-MM-DD format
    title: str = Field(primary_key=True)

    url: Optional[str] = None
