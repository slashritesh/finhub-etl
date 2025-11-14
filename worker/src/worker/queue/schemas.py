"""
Task Schemas for RabbitMQ Messages

Defines the structure of messages that workers will process.
"""

from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl


class BaseTask(BaseModel):
    """Base task schema with common fields."""
    task_id: str = Field(..., description="Unique identifier for this task")
    task_type: str = Field(..., description="Type of task to execute")
    priority: int = Field(default=5, ge=1, le=10, description="Task priority (1=highest, 10=lowest)")


class FetchTask(BaseTask):
    """
    Task for fetching data from an API.

    Example message:
    {
        "task_id": "task_123",
        "task_type": "fetch_company_profile",
        "symbol": "AAPL",
        "endpoint": "/stock/profile2",
        "params": {"isin": "US0378331005"}
    }
    """
    task_type: Literal["fetch_company_profile", "fetch_quote", "fetch_news", "fetch_custom"]
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL)")
    endpoint: Optional[str] = Field(None, description="API endpoint to call")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional query parameters")


class UrlFetchTask(BaseTask):
    """
    Task for fetching data from a direct URL.

    Example message:
    {
        "task_id": "task_456",
        "task_type": "fetch_from_url",
        "url": "https://api.example.com/data",
        "method": "GET",
        "headers": {"Authorization": "Bearer token"},
        "params": {"symbol": "AAPL"}
    }
    """
    task_type: Literal["fetch_from_url"]
    url: str = Field(..., description="Full URL to fetch from")
    method: Literal["GET", "POST"] = Field(default="GET", description="HTTP method")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="HTTP headers")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Query parameters or body")


class BulkFetchTask(BaseTask):
    """
    Task for fetching data for multiple symbols.

    Example message:
    {
        "task_id": "task_789",
        "task_type": "bulk_fetch",
        "symbols": ["AAPL", "GOOGL", "MSFT"],
        "data_type": "quote",
        "from_date": "2024-01-01",
        "to_date": "2024-01-31"
    }
    """
    task_type: Literal["bulk_fetch"]
    symbols: list[str] = Field(..., description="List of stock symbols")
    data_type: str = Field(..., description="Type of data to fetch (e.g., quote, profile, news)")
    from_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    to_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    extra_params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional parameters")


class GenericTask(BaseTask):
    """
    Generic task for custom processing.

    Example message:
    {
        "task_id": "task_999",
        "task_type": "custom_processing",
        "handler": "company.get_company_profile2",
        "model": "CompanyProfile2",
        "params": {"symbol": "AAPL"}
    }
    """
    task_type: str
    handler: str = Field(..., description="Handler function path (e.g., 'company.get_company_profile2')")
    model: str = Field(..., description="Model name (e.g., 'CompanyProfile2')")
    params: Dict[str, Any] = Field(..., description="Parameters to pass to handler")


# Union type for all task types
Task = FetchTask | UrlFetchTask | BulkFetchTask | GenericTask
