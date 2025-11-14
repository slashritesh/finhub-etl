from typing import Optional
from sqlmodel import SQLModel, Field


class CompanyExecutive(SQLModel, table=True):
    """Company Executive - /stock/executive"""
    __tablename__ = "company_executives"

    # Composite Primary Key
    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)

    # Fields from the API
    age: Optional[int] = None
    compensation: Optional[int] = None
    currency: Optional[str] = None
    position: Optional[str] = None
    sex: Optional[str] = None
    since: Optional[str] = None