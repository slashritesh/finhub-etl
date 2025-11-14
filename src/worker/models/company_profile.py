from typing import Optional
from sqlmodel import Column, SQLModel, Field, Text


class CompanyProfile(SQLModel, table=True):
    """Company Profile (v1) - /stock/profile"""
    __tablename__ = "company_profiles"

    ticker: str = Field(primary_key=True)
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None
    weburl: Optional[str] = None
    logo: Optional[str] = None
    naics: Optional[str] = None
    naics_national_industry: Optional[str] = Field(default=None, alias="naicsNationalIndustry")
    naics_sector: Optional[str] = Field(default=None, alias="naicsSector")
    naics_subsector: Optional[str] = Field(default=None, alias="naicsSubsector")
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    exchange: Optional[str] = None
    ipo: Optional[str] = None
    market_capitalization: Optional[float] = Field(default=None, alias="marketCapitalization")
    share_outstanding: Optional[float] = Field(default=None, alias="shareOutstanding")
    employee_total: Optional[int] = Field(default=None, alias="employeeTotal")
    ggroup: Optional[str] = None
    gind: Optional[str] = None
    gsector: Optional[str] = None
    gsubind: Optional[str] = None
    cusip: Optional[str] = None
    isin: Optional[str] = None
    lei: Optional[str] = None
    sedol: Optional[str] = None
    
    # ADDED a field for "currency" 
    currency: Optional[str] = None
    
    #  ADDED a field for "finnhubIndustry"
    finnhub_industry: Optional[str] = Field(default=None, alias="finnhubIndustry")


class CompanyProfile2(SQLModel, table=True):
    """Company Profile (v2) - /stock/profile2"""
    __tablename__ = "company_profiles_v2"

    ticker: str = Field(primary_key=True)
    name: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    ipo: Optional[str] = None
    market_capitalization: Optional[float] = Field(default=None, alias="marketCapitalization")
    phone: Optional[str] = None
    share_outstanding: Optional[float] = Field(default=None, alias="shareOutstanding")
    weburl: Optional[str] = None
    logo: Optional[str] = None
    finnhub_industry: Optional[str] = Field(default=None, alias="finnhubIndustry")
