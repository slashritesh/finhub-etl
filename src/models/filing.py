from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyFiling(SQLModel, table=True):
    """Company Filings - /stock/filings"""
    __tablename__ = "company_filings"

    symbol: str = Field(primary_key=True, index=True)
    access_number: str = Field(primary_key=True, alias="accessNumber")

    cik: Optional[str] = None
    form: Optional[str] = None
    filed_date: Optional[str] = Field(default=None, alias="filedDate")
    accepted_date: Optional[str] = Field(default=None, alias="acceptedDate")
    report_url: Optional[str] = Field(default=None, alias="reportUrl")
    filing_url: Optional[str] = Field(default=None, alias="filingUrl")
