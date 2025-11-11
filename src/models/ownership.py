from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyOwnership(SQLModel, table=True):
    """Company Ownership - /stock/ownership"""
    __tablename__ = "company_ownership"

    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)
    change: Optional[float] = None
    filing_date: Optional[str] = Field(default=None, alias="filingDate")
    share: Optional[int] = None


class FundOwnership(SQLModel, table=True):
    """Fund Ownership - /stock/fund-ownership"""
    __tablename__ = "fund_ownership"

    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)
    change: Optional[float] = None
    filing_date: Optional[str] = Field(default=None, alias="filingDate")
    portfolio_percent: Optional[float] = Field(default=None, alias="portfolioPercent")
    share: Optional[int] = None
    value: Optional[float] = None


class InstitutionalOwnership(SQLModel, table=True):
    """Institutional Ownership - /institutional/ownership"""
    __tablename__ = "institutional_ownership"

    symbol: str = Field(primary_key=True, index=True)
    cik: str = Field(primary_key=True)
    name: str
    change: Optional[float] = None
    filing_date: Optional[str] = Field(default=None, alias="filingDate")
    no_voting: Optional[int] = Field(default=None, alias="noVoting")
    portfolio_percent: Optional[float] = Field(default=None, alias="portfolioPercent")
    share: Optional[int] = None
    shared_voting: Optional[int] = Field(default=None, alias="sharedVoting")
    sole_voting: Optional[int] = Field(default=None, alias="soleVoting")
    value: Optional[float] = None
