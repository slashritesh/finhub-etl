"""
RabbitMQ Consumer

Listens to queues and processes incoming tasks.
"""

import json
import asyncio
from typing import Callable, Optional
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractQueue
from pydantic import ValidationError

from .connection import rabbitmq
from .schemas import Task, FetchTask, UrlFetchTask, BulkFetchTask, GenericTask
from .processor import processor


class TaskConsumer:
    """Consumes tasks from RabbitMQ and processes them."""

    def __init__(self, queue_name: str = "finhub_tasks"):
        self.queue_name = queue_name
        self.queue: Optional[AbstractQueue] = None
        self.is_running = False

    async def start(self):
        """Start consuming messages from the queue."""
        print(f"🚀 Starting consumer for queue: {self.queue_name}")

        # Get channel
        channel = await rabbitmq.get_channel()

        # Declare queue (creates if doesn't exist)
        self.queue = await channel.declare_queue(
            self.queue_name,
            durable=True,  # Survive broker restart
            arguments={
                "x-message-ttl": 86400000,  # Messages expire after 24 hours
                "x-max-length": 10000,      # Max 10k messages in queue
            }
        )

        print(f"📬 Queue '{self.queue_name}' ready")
        print(f"💬 Waiting for messages... (Press CTRL+C to exit)")

        # Start consuming
        self.is_running = True
        await self.queue.consume(self._on_message)

    async def _on_message(self, message: IncomingMessage):
        """
        Callback when a message is received.

        Args:
            message: Incoming RabbitMQ message
        """
        async with message.process():
            try:
                # Parse message body
                body = json.loads(message.body.decode())
                print(f"\n📨 Received message: {body.get('task_id', 'unknown')}")

                # Validate and parse task
                task = self._parse_task(body)

                # Process the task
                result = await processor.process(task)

                print(f"✅ Message processed: {result.get('status')}")

            except ValidationError as e:
                print(f"❌ Invalid message format: {e}")
            except Exception as e:
                print(f"❌ Error processing message: {str(e)}")
                # Message will be requeued or sent to DLQ based on your RabbitMQ config

    def _parse_task(self, data: dict) -> Task:
        """
        Parse and validate incoming message data.

        Args:
            data: Raw message dictionary

        Returns:
            Validated Task object
        """
        task_type = data.get("task_type")

        # Route to appropriate schema based on task_type
        if task_type in ["fetch_company_profile", "fetch_quote", "fetch_news", "fetch_custom"]:
            return FetchTask(**data)
        elif task_type == "fetch_from_url":
            return UrlFetchTask(**data)
        elif task_type == "bulk_fetch":
            return BulkFetchTask(**data)
        else:
            # Default to GenericTask
            return GenericTask(**data)

    async def stop(self):
        """Stop consuming messages."""
        self.is_running = False
        print("\n🛑 Stopping consumer...")
        await rabbitmq.close()


async def run_consumer(queue_name: str = "finhub_tasks"):
    """
    Run the consumer (main entry point).

    Args:
        queue_name: Name of the RabbitMQ queue to consume from
    """
    consumer = TaskConsumer(queue_name=queue_name)

    try:
        await consumer.start()

        # Keep running until interrupted
        while consumer.is_running:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n⚠️ Received interrupt signal")
    finally:
        await consumer.stop()
        print("👋 Consumer stopped")


if __name__ == "__main__":
    asyncio.run(run_consumer())
