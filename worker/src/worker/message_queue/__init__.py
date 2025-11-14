"""
RabbitMQ Queue Module

Provides RabbitMQ connection, consumer, producer, and task schemas.
"""

from .connection import rabbitmq, RabbitMQConnection
from .consumer import TaskConsumer, run_consumer
from .connection_aio import async_rabbitmq, AsyncRabbitMQConnection
from .consumer_aio import AsyncTaskConsumer, run_consumer as run_consumer_async

__all__ = [
    # Sync Connection
    "rabbitmq",
    "RabbitMQConnection",
    # Sync Consumer
    "TaskConsumer",
    "run_consumer",
    # Async Connection
    "async_rabbitmq",
    "AsyncRabbitMQConnection",
    # Async Consumer
    "AsyncTaskConsumer",
    "run_consumer_async",
]
