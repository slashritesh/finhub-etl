from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class StockSymbol(SQLModel, table=True):
    """Stock symbols and exchange information.

    API Response fields: symbol, description, displaySymbol, type, currency, figi, mic
    """

    __tablename__ = "stock_symbols"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(unique=True, index=True, max_length=10)
    description: Optional[str] = Field(default=None, max_length=200)
    displaySymbol: Optional[str] = Field(default=None, max_length=20)

    type: Optional[str] = Field(default=None, max_length=50)  # 'Common Stock', 'ETF', etc.
    currency: Optional[str] = Field(default=None, max_length=10)

    figi: Optional[str] = Field(default=None, max_length=20)
    mic: Optional[str] = Field(default=None, max_length=10)

    # Extra field for exchange context
    exchange: Optional[str] = Field(default=None, max_length=50, index=True)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class CompanyExecutive(SQLModel, table=True):
    """Company executive officers information.

    API Response fields: name, age, title, since, compensation, currency, sex
    """

    __tablename__ = "company_executives"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)

    name: Optional[str] = Field(default=None, max_length=200)
    age: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None, max_length=200)
    since: Optional[str] = Field(default=None, max_length=20)  # Year started

    compensation: Optional[float] = Field(default=None)
    currency: Optional[str] = Field(default=None, max_length=10)
    sex: Optional[str] = Field(default=None, max_length=10)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class CompanyPeer(SQLModel, table=True):
    """Peer companies relationships.

    API Response is array of peer symbols
    """

    __tablename__ = "company_peers"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    peer: str = Field(index=True, max_length=10)

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
