from typing import Optional
from sqlmodel import SQLModel, Field


class Dividend(SQLModel, table=True):
    """Dividends - /stock/dividend"""
    __tablename__ = "dividends"

    symbol: str = Field(primary_key=True, index=True)
    date: str = Field(primary_key=True)  # Ex-dividend date

    amount: Optional[float] = None
    adjusted_amount: Optional[float] = Field(default=None, alias="adjustedAmount")
    currency: Optional[str] = None
    declaration_date: Optional[str] = Field(default=None, alias="declarationDate")
    payment_date: Optional[str] = Field(default=None, alias="paymentDate")
    record_date: Optional[str] = Field(default=None, alias="recordDate")
