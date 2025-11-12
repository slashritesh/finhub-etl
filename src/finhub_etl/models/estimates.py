from typing import Optional
from sqlmodel import SQLModel, Field


class RevenueEstimate(SQLModel, table=True):
    """Revenue Estimate - /stock/revenue-estimate"""
    __tablename__ = "revenue_estimates"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    revenue_avg: Optional[float] = Field(default=None, alias="revenueAvg")
    revenue_high: Optional[float] = Field(default=None, alias="revenueHigh")
    revenue_low: Optional[float] = Field(default=None, alias="revenueLow")
    number_analysts: Optional[int] = Field(default=None, alias="numberAnalysts")
    
    # fix
    quarter: Optional[int] = None
    year: Optional[int] = None


class EpsEstimate(SQLModel, table=True):
    """EPS Estimate - /stock/eps-estimate"""
    __tablename__ = "eps_estimates"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    eps_avg: Optional[float] = Field(default=None, alias="epsAvg")
    eps_high: Optional[float] = Field(default=None, alias="epsHigh")
    eps_low: Optional[float] = Field(default=None, alias="epsLow")
    number_analysts: Optional[int] = Field(default=None, alias="numberAnalysts")


class EbitdaEstimate(SQLModel, table=True):
    """EBITDA Estimate - /stock/ebitda-estimate"""
    __tablename__ = "ebitda_estimates"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    ebitda_avg: Optional[float] = Field(default=None, alias="ebitdaAvg")
    ebitda_high: Optional[float] = Field(default=None, alias="ebitdaHigh")
    ebitda_low: Optional[float] = Field(default=None, alias="ebitdaLow")
    number_analysts: Optional[int] = Field(default=None, alias="numberAnalysts")


class EbitEstimate(SQLModel, table=True):
    """EBIT Estimate - /stock/ebit-estimate"""
    __tablename__ = "ebit_estimates"

    symbol: str = Field(primary_key=True, index=True)
    period: str = Field(primary_key=True)

    ebit_avg: Optional[float] = Field(default=None, alias="ebitAvg")
    ebit_high: Optional[float] = Field(default=None, alias="ebitHigh")
    ebit_low: Optional[float] = Field(default=None, alias="ebitLow")
    number_analysts: Optional[int] = Field(default=None, alias="numberAnalysts")
