from typing import Optional
from sqlmodel import Column, SQLModel, Field, Text

class PressRelease(SQLModel, table=True):
    __tablename__ = "press_releases"

    # Composite primary key (unique per symbol + datetime)
    symbol: str = Field(primary_key=True)
    datetime: str = Field(primary_key=True, alias="datetime")  # "2020-08-04 17:06:32"

    # Data fields
    headline: Optional[str] = None
    description: Optional[str] = Field(default=None,sa_column=Column(Text))
    url: Optional[str] = None