from typing import Optional
from sqlmodel import SQLModel, Field


class InsiderTransaction(SQLModel, table=True):
    """Insider Transactions - /stock/insider-transactions"""
    __tablename__ = "insider_transactions"

    symbol: str = Field(primary_key=True, index=True)
    name: str = Field(primary_key=True)
    filing_date: str = Field(primary_key=True, alias="filingDate")
    transaction_date: str = Field(primary_key=True, alias="transactionDate")

    share: Optional[float] = None
    change: Optional[float] = None
    transaction_code: Optional[str] = Field(default=None, alias="transactionCode")
    transaction_price: Optional[float] = Field(default=None, alias="transactionPrice")
