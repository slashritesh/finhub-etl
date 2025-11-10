from typing import Optional
from sqlmodel import SQLModel, Field


class InstitutionalProfile(SQLModel, table=True):
    """Institutional Profile - /institutional/profile"""
    __tablename__ = "institutional_profiles"

    cik: str = Field(primary_key=True)
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    manager: Optional[str] = None
    phone: Optional[str] = None
    profile: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None


class InstitutionalPortfolio(SQLModel, table=True):
    """Institutional Portfolio - /institutional/portfolio"""
    __tablename__ = "institutional_portfolios"

    cik: str = Field(primary_key=True, index=True)
    symbol: str = Field(primary_key=True)
    filing_date: str = Field(primary_key=True, alias="filingDate")

    name: str
    change: Optional[float] = None
    no_voting: Optional[int] = Field(default=None, alias="noVoting")
    share: Optional[int] = None
    shared_voting: Optional[int] = Field(default=None, alias="sharedVoting")
    sole_voting: Optional[int] = Field(default=None, alias="soleVoting")
    value: Optional[float] = None
