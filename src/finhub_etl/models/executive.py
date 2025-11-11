from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyExecutive(SQLModel, table=True):
    """Company Executives - /stock/executive"""
    __tablename__ = "company_executives"

    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)

    age: Optional[int] = None
    title: Optional[str] = None
    since: Optional[str] = None
    sex: Optional[str] = None
    compensation: Optional[float] = None
    currency: Optional[str] = None
