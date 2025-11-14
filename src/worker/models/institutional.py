from typing import Optional
from sqlmodel import SQLModel, Field, Column, Text


class InstitutionalProfile(SQLModel, table=True):
    """Institutional Profile - /institutional/profile"""
    __tablename__ = "institutional_profiles"
    __table_args__ = {"extend_existing": True}

    # Primary Key
    cik: str = Field(primary_key=True)

    # All fields from the API response
    firm_type: Optional[str] = Field(default=None, alias="firmType")
    manager: Optional[str] = None
    philosophy: Optional[str] = Field(default=None, sa_column=Column(Text))
    profile: Optional[str] = Field(default=None, sa_column=Column(Text))
    profile_img: Optional[str] = Field(default=None, alias="profileImg")


class InstitutionalPortfolio(SQLModel, table=True):
    __tablename__ = "institutional_portfolios"

    cik: str = Field(primary_key=True)
    symbol: str = Field(primary_key=True)          # portfolio item
    filing_date: str = Field(primary_key=True, alias="filingDate")

    institution_name: str = Field(alias="name")    # firm name
    report_date: str = Field(alias="reportDate")

    change: Optional[int] = None
    no_voting: Optional[int] = Field(default=None, alias="noVoting")
    percentage: Optional[float] = None
    put_call: Optional[str] = Field(default=None, alias="putCall")
    share: Optional[int] = None
    shared_voting: Optional[int] = Field(default=None, alias="sharedVoting")
    sole_voting: Optional[int] = Field(default=None, alias="soleVoting")
    value: Optional[float] = None

    