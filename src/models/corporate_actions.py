from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Dividend(SQLModel, table=True):
    """Stock dividend data.

    API Response fields: symbol, date, amount, adjustedAmount, payDate, recordDate, declarationDate, currency
    """

    __tablename__ = "dividends"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    date: str = Field(index=True, max_length=20)  # Ex-dividend date
    amount: float
    adjustedAmount: Optional[float] = Field(default=None)
    payDate: Optional[str] = Field(default=None, max_length=20)
    recordDate: Optional[str] = Field(default=None, max_length=20)
    declarationDate: Optional[str] = Field(default=None, max_length=20)
    currency: Optional[str] = Field(default=None, max_length=10)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class StockSplit(SQLModel, table=True):
    """Stock split history.

    API Response fields: symbol, date, fromFactor, toFactor
    """

    __tablename__ = "stock_splits"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    date: str = Field(index=True, max_length=20)  # Split date
    fromFactor: float  # Split from
    toFactor: float  # Split to

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class SecFiling(SQLModel, table=True):
    """SEC filings data.

    API Response fields: accessNumber, symbol, cik, form, filedDate, acceptedDate, reportUrl, filingUrl
    """

    __tablename__ = "sec_filings"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    accessNumber: Optional[str] = Field(default=None, max_length=50, unique=True)
    cik: Optional[str] = Field(default=None, max_length=20, index=True)
    form: str = Field(max_length=20, index=True)  # Form type (e.g., '10-K', '10-Q', '8-K')
    filedDate: str = Field(index=True, max_length=20)
    acceptedDate: Optional[str] = Field(default=None, max_length=50)
    reportUrl: Optional[str] = Field(default=None, max_length=500)
    filingUrl: Optional[str] = Field(default=None, max_length=500)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
