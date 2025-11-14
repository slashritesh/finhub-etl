from typing import Optional
from sqlmodel import SQLModel, Field


class HistoricalEmployeeCount(SQLModel, table=True):
    """Historical Employee Count - /stock/historical-employee-count"""
    __tablename__ = "historical_employee_count"

    symbol: str = Field(primary_key=True, index=True)
    period_date: str = Field(primary_key=True) 

    # Data Fields
    employee_count: Optional[int] = None 
