from typing import Optional
from sqlmodel import SQLModel, Field

class StockSymbol(SQLModel, table=True):
    symbol: str = Field(primary_key=True, nullable=False)
    display_symbol: Optional[str] = Field(default=None, alias="displaySymbol")
    description: Optional[str] = None
    currency: Optional[str] = None
    figi: Optional[str] = None
    mic: Optional[str] = None
    type: Optional[str] = None
