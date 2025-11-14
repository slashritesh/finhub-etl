from typing import Any, Dict, Optional
from sqlmodel import JSON, Column, SQLModel, Field


class SectorMetrics(SQLModel, table=True):
    __tablename__ = "sector_metrics"

    # Composite primary key
    sector: str = Field(primary_key=True)
    region: str = Field(primary_key=True)

    # Store ALL metric key-values as JSON
    metrics: Dict[str, Any] = Field(default_factory=dict,sa_column=Column(JSON))