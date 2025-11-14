"""
Worker Main Entry Point

Starts the RabbitMQ consumer to process tasks.

Usage:
    python -m worker.main
"""

import asyncio
import os
from dotenv import load_dotenv
from worker.queue import run_consumer

load_dotenv()


async def main():
    """Main worker process."""
    queue_name = os.getenv("RABBITMQ_QUEUE", "finhub_tasks")

    print("=" * 60)
    print("<í Finhub ETL Worker")
    print("=" * 60)
    print(f"Queue: {queue_name}")
    print(f"Database: {os.getenv('DATABASE_URL', 'Not configured')[:50]}...")
    print("=" * 60)

    # Start consuming tasks
    await run_consumer(queue_name=queue_name)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n=K Worker shutdown complete")
