from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class InsiderTransaction(SQLModel, table=True):
    """Insider trading transactions.

    API Response fields: id, symbol, name, share, change, filingDate, transactionDate, transactionCode, transactionPrice
    """

    __tablename__ = "insider_transactions"

    id: str = Field(primary_key=True, max_length=50)  # Changed to string to match API transaction IDs
    symbol: str = Field(index=True, max_length=10)
    transactionDate: str = Field(index=True, max_length=20)
    filingDate: Optional[str] = Field(default=None, max_length=20)

    name: Optional[str] = Field(default=None, max_length=200)
    share: Optional[float] = Field(default=None)
    change: Optional[float] = Field(default=None)
    transactionCode: Optional[str] = Field(default=None, max_length=10)
    transactionPrice: Optional[float] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class InstitutionalOwnership(SQLModel, table=True):
    """Institutional ownership data.

    API Response fields: symbol, cik, name, reportDate, filingDate, share, change, portfolioPercent
    """

    __tablename__ = "institutional_ownership"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: Optional[str] = Field(index=True, max_length=10)
    cik: Optional[str] = Field(default=None, max_length=20, index=True)
    name: Optional[str] = Field(default=None, max_length=200)

    reportDate: Optional[str] = Field(default=None, max_length=20, index=True)
    filingDate: Optional[str] = Field(default=None, max_length=20)

    share: Optional[float] = Field(default=None)
    change: Optional[float] = Field(default=None)
    portfolioPercent: Optional[float] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class FundOwnership(SQLModel, table=True):
    """Mutual fund and ETF ownership data.

    API Response fields: symbol, name, reportDate, share, change, portfolioPercent
    """

    __tablename__ = "fund_ownership"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    name: Optional[str] = Field(default=None, max_length=200)

    reportDate: Optional[str] = Field(default=None, max_length=20, index=True)

    share: Optional[float] = Field(default=None)
    change: Optional[float] = Field(default=None)
    portfolioPercent: Optional[float] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class InstitutionalProfile(SQLModel, table=True):
    """Institutional investor profiles.

    API Response fields: cik, name, manager
    """

    __tablename__ = "institutional_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    cik: str = Field(unique=True, max_length=20, index=True)
    name: Optional[str] = Field(default=None, max_length=200)
    manager: Optional[str] = Field(default=None, max_length=200)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class InstitutionalPortfolio(SQLModel, table=True):
    """Institutional portfolio holdings.

    API Response fields: cik, symbol, reportDate, filingDate, cusip, share, value, change
    """

    __tablename__ = "institutional_portfolios"

    id: Optional[int] = Field(default=None, primary_key=True)
    cik: str = Field(index=True, max_length=20)
    symbol: str = Field(index=True, max_length=10)

    reportDate: str = Field(index=True, max_length=20)
    filingDate: Optional[str] = Field(default=None, max_length=20)

    cusip: Optional[str] = Field(default=None, max_length=20)
    share: Optional[float] = Field(default=None)
    value: Optional[float] = Field(default=None)
    change: Optional[float] = Field(default=None)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
