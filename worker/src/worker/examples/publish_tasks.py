"""
Example: How to Publish Tasks to RabbitMQ

This shows various ways to publish tasks to the worker queue.

Usage:
    python -m worker.examples.publish_tasks
"""

import asyncio
from worker.queue import publish_task, TaskProducer
from worker.queue.schemas import FetchTask, UrlFetchTask, BulkFetchTask, GenericTask


async def example_1_fetch_company_profile():
    """Example 1: Fetch company profile for a single symbol."""
    print("\n=== Example 1: Fetch Company Profile ===")

    task = FetchTask(
        task_id="task_001",
        task_type="fetch_company_profile",
        symbol="AAPL",
        params={},  # Optional additional params
        priority=5,
    )

    await publish_task(task)
    print("✅ Published company profile task")


async def example_2_fetch_from_url():
    """Example 2: Fetch data from a custom URL."""
    print("\n=== Example 2: Fetch from URL ===")

    task = UrlFetchTask(
        task_id="task_002",
        task_type="fetch_from_url",
        url="https://api.example.com/data",
        method="GET",
        headers={"Authorization": "Bearer YOUR_TOKEN"},
        params={"symbol": "AAPL", "date": "2024-01-01"},
        priority=3,
    )

    await publish_task(task)
    print("✅ Published URL fetch task")


async def example_3_bulk_fetch():
    """Example 3: Fetch data for multiple symbols."""
    print("\n=== Example 3: Bulk Fetch ===")

    task = BulkFetchTask(
        task_id="task_003",
        task_type="bulk_fetch",
        symbols=["AAPL", "GOOGL", "MSFT", "TSLA"],
        data_type="quote",
        from_date="2024-01-01",
        to_date="2024-01-31",
        priority=7,
    )

    await publish_task(task)
    print("✅ Published bulk fetch task")


async def example_4_generic_task():
    """Example 4: Generic task with custom handler."""
    print("\n=== Example 4: Generic Task ===")

    task = GenericTask(
        task_id="task_004",
        task_type="custom_processing",
        handler="company.get_company_profile2",
        model="company_profile.CompanyProfile2",
        params={"symbol": "AAPL"},
        priority=5,
    )

    await publish_task(task)
    print("✅ Published generic task")


async def example_5_batch_publish():
    """Example 5: Publish multiple tasks at once."""
    print("\n=== Example 5: Batch Publish ===")

    tasks = [
        {
            "task_id": f"task_batch_{i}",
            "task_type": "fetch_company_profile",
            "symbol": symbol,
            "params": {},
            "priority": 5,
        }
        for i, symbol in enumerate(["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"])
    ]

    producer = TaskProducer(queue_name="finhub_tasks")
    await producer.publish_batch(tasks)
    print(f"✅ Published {len(tasks)} tasks")


async def example_6_dict_format():
    """Example 6: Publish using dictionary format (no Pydantic)."""
    print("\n=== Example 6: Dictionary Format ===")

    task_dict = {
        "task_id": "task_006",
        "task_type": "fetch_company_profile",
        "symbol": "NVDA",
        "params": {"isin": "US67066G1040"},
        "priority": 4,
    }

    await publish_task(task_dict)
    print("✅ Published task from dictionary")


async def main():
    """Run all examples."""
    print("🚀 Publishing Example Tasks to RabbitMQ")
    print("=" * 60)

    # Uncomment the examples you want to run

    await example_1_fetch_company_profile()
    # await example_2_fetch_from_url()
    # await example_3_bulk_fetch()
    # await example_4_generic_task()
    # await example_5_batch_publish()
    # await example_6_dict_format()

    print("\n" + "=" * 60)
    print("✨ All tasks published!")
    print("💡 Start the worker with: python -m worker.main")


if __name__ == "__main__":
    asyncio.run(main())
