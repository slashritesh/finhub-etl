from typing import Optional
from sqlmodel import SQLModel, Field

class CompanyOwnership(SQLModel, table=True):
    """Company Ownership - /stock/ownership"""
    __tablename__ = "company_ownership"
    __table_args__ = {"extend_existing": True}

    # Composite Primary Key
    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)

    # Fields from the API response
    change: Optional[int] = None # API shows integer values
    filing_date: Optional[str] = Field(default=None, alias="filingDate")
    share: Optional[int] = None


class FundOwnership(SQLModel, table=True):
    """Fund Ownership - /stock/fund-ownership"""
    __tablename__ = "fund_ownership"
    __table_args__ = {"extend_existing": True}

    # Composite Primary Key
    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)

    # Fields from the API response
    change: Optional[int] = None # The API response shows integers, not floats
    filing_date: Optional[str] = Field(default=None, alias="filingDate")
    portfolio_percent: Optional[float] = Field(default=None, alias="portfolioPercent")
    share: Optional[int] = None
    
    # The 'value' field was removed as it is not in the API response


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
