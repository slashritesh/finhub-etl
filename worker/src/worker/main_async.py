"""
Worker Main Entry Point (Async version using aio-pika)

Starts the async RabbitMQ consumer to process tasks.

Usage:
    python -m worker.main_async
"""

import asyncio
import os
from dotenv import load_dotenv
from worker.message_queue import run_consumer_async

load_dotenv()


async def main():
    """Main worker process."""
    queue_name = os.getenv("RABBITMQ_QUEUE", "finhub_tasks")

    print("=" * 60)
    print("Finhub ETL Worker (Async)")
    print("=" * 60)
    print(f"Queue: {queue_name}")
    print(f"Database: {os.getenv('DATABASE_URL', 'Not configured')[:50]}...")
    print("=" * 60)

    # Start consuming tasks
    await run_consumer_async(queue_name=queue_name)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Worker shutdown complete")
