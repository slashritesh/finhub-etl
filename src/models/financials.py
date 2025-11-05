from datetime import datetime as dt, timezone
from typing import Optional
from sqlmodel import Field, SQLModel, JSON, Column


class FinancialReportData(SQLModel, table=True):
    """Financial reports as filed (as reported).

    API Response fields: symbol, cik, year, quarter, form, startDate, endDate, filedDate, acceptedDate, report
    """

    __tablename__ = "financial_report_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    cik: Optional[str] = Field(default=None, max_length=20, index=True)
    year: int = Field(index=True)
    quarter: Optional[int] = Field(default=None, index=True)  # 0 for annual, 1-4 for quarters
    form: Optional[str] = Field(default=None, max_length=20)  # e.g., '10-K', '10-Q'

    startDate: Optional[str] = Field(default=None, max_length=20)
    endDate: Optional[str] = Field(default=None, max_length=20)
    filedDate: Optional[str] = Field(default=None, max_length=20)
    acceptedDate: Optional[str] = Field(default=None, max_length=50)
    accessNumber: Optional[str] = Field(default=None, max_length=50)

    report: Optional[dict] = Field(default=None, sa_column=Column(JSON))  # Full report data
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class BasicFinancials(SQLModel, table=True):
    """Basic financial metrics and ratios.

    API Response has 'metric' and 'series' top-level keys with various nested fields
    """

    __tablename__ = "basic_financials"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10, unique=True)

    # Store full metric and series data as JSON
    metric: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    series: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    updated_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))


class FinancialsStandardized(SQLModel, table=True):
    """Standardized financial statements (income, balance, cash flow).

    API Response fields: symbol, cik, year, quarter, currency, data (array)
    """

    __tablename__ = "financials_standardized"

    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str = Field(index=True, max_length=10)
    statement: str = Field(max_length=20)  # 'income', 'balance', 'cash'
    freq: str = Field(max_length=10)  # 'annual' or 'quarterly'

    cik: Optional[str] = Field(default=None, max_length=20)
    year: Optional[int] = Field(default=None, index=True)
    quarter: Optional[int] = Field(default=None)
    currency: Optional[str] = Field(default=None, max_length=10)

    # Store full data array as JSON
    data: Optional[dict] = Field(default=None, sa_column=Column(JSON))

    created_at: dt = Field(default_factory=lambda: dt.now(timezone.utc))
