from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class CompanyProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None
    cusip: Optional[str] = None
    sedol: Optional[str] = None
    isin: Optional[str] = None
    description: Optional[str] = None
    employeeTotal: Optional[int] = None
    exchange: Optional[str] = None
    ggroup: Optional[str] = None
    gind: Optional[str] = None
    gsector: Optional[str] = None
    gsubind: Optional[str] = None
    ipo: Optional[date] = None
    marketCapitalization: Optional[float] = None
    naics: Optional[str] = None
    naicsNationalIndustry: Optional[str] = None
    naicsSector: Optional[str] = None
    naicsSubsector: Optional[str] = None
    name: Optional[str] = None
    ticker: Optional[str] = None
    finnhubIndustry: Optional[str] = None
    phone: Optional[str] = None
    weburl: Optional[str] = None
    logo: Optional[str] = None
    shareOutstanding: Optional[float] = None
