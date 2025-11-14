"""
RabbitMQ Queue Module

Provides RabbitMQ connection, consumer, producer, and task schemas.
"""

from .connection import rabbitmq, RabbitMQConnection
from .consumer import TaskConsumer, run_consumer
from .producer import TaskProducer, publish_task
from .processor import processor, TaskProcessor
from .schemas import (
    Task,
    BaseTask,
    FetchTask,
    UrlFetchTask,
    BulkFetchTask,
    GenericTask,
)

__all__ = [
    # Connection
    "rabbitmq",
    "RabbitMQConnection",
    # Consumer
    "TaskConsumer",
    "run_consumer",
    # Producer
    "TaskProducer",
    "publish_task",
    # Processor
    "processor",
    "TaskProcessor",
    # Schemas
    "Task",
    "BaseTask",
    "FetchTask",
    "UrlFetchTask",
    "BulkFetchTask",
    "GenericTask",
]
