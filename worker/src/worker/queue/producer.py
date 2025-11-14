"""
RabbitMQ Producer

Publishes tasks to RabbitMQ queues.
"""

import json
from typing import Dict, Any
from aio_pika import Message, DeliveryMode

from .connection import rabbitmq
from .schemas import Task


class TaskProducer:
    """Publishes tasks to RabbitMQ queues."""

    def __init__(self, queue_name: str = "finhub_tasks"):
        self.queue_name = queue_name

    async def publish(self, task: Task | Dict[str, Any], routing_key: str = None):
        """
        Publish a task to the queue.

        Args:
            task: Task object or dictionary
            routing_key: Optional routing key (defaults to queue_name)
        """
        # Convert task to dict if it's a Pydantic model
        if hasattr(task, "model_dump"):
            task_dict = task.model_dump()
        else:
            task_dict = task

        # Get channel
        channel = await rabbitmq.get_channel()

        # Declare queue
        await channel.declare_queue(self.queue_name, durable=True)

        # Create message
        message = Message(
            body=json.dumps(task_dict).encode(),
            delivery_mode=DeliveryMode.PERSISTENT,  # Survive broker restart
            content_type="application/json",
        )

        # Publish to default exchange with queue name as routing key
        await channel.default_exchange.publish(
            message,
            routing_key=routing_key or self.queue_name,
        )

        print(f"📤 Published task: {task_dict.get('task_id')} to queue '{self.queue_name}'")

    async def publish_batch(self, tasks: list[Task | Dict[str, Any]]):
        """
        Publish multiple tasks at once.

        Args:
            tasks: List of Task objects or dictionaries
        """
        for task in tasks:
            await self.publish(task)

        print(f"📤 Published {len(tasks)} tasks to queue '{self.queue_name}'")


# Convenience function
async def publish_task(task: Task | Dict[str, Any], queue_name: str = "finhub_tasks"):
    """
    Quick helper to publish a single task.

    Args:
        task: Task object or dictionary
        queue_name: Name of the queue to publish to
    """
    producer = TaskProducer(queue_name=queue_name)
    await producer.publish(task)
