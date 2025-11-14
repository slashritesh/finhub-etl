"""
Example Worker - Minimal boilerplate for fetching and storing data

This demonstrates the complete workflow:
1. Fetch data from an API
2. Store it in the database
3. Handle errors gracefully

Run this file to test: python -m worker.example_worker
"""

import asyncio
from worker.config.handlers.example import (
    fetch_simple_data,
    fetch_data_with_options,
    fetch_and_flatten,
)
from worker.models.example_data import ExampleData
from worker.utils.save import fetch_and_store_data


async def example_1_simple():
    """Example 1: Fetch and store simple data"""
    print("\n=== Example 1: Simple Fetch & Store ===")

    # Note: This will fail with a real API call since it's example.com
    # Replace with your actual endpoint
    try:
        result = await fetch_and_store_data(
            handler=fetch_simple_data,
            model=ExampleData,
            symbol="AAPL",
            endpoint="https://api.example.com/data"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error (example endpoint): {e}")


async def example_2_with_optional_params():
    """Example 2: Fetch with optional parameters"""
    print("\n=== Example 2: With Optional Parameters ===")

    try:
        result = await fetch_and_store_data(
            handler=fetch_data_with_options,
            model=ExampleData,
            symbol="AAPL",
            data_type="metrics",
            from_date="2024-01-01",  # Optional
            to_date="2024-01-31",    # Optional
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error (example endpoint): {e}")


async def example_3_nested_response():
    """Example 3: Handle nested API response"""
    print("\n=== Example 3: Nested Response ===")

    try:
        result = await fetch_and_store_data(
            handler=fetch_and_flatten,
            model=ExampleData,
            symbol="AAPL",
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error (example endpoint): {e}")


async def example_4_manual_workflow():
    """Example 4: Manual workflow without the helper function"""
    print("\n=== Example 4: Manual Workflow ===")

    from sqlmodel.ext.asyncio.session import AsyncSession
    from worker.database import engine

    async with AsyncSession(engine) as session:
        try:
            # Step 1: Fetch data from API
            # (Using dummy data since example.com won't work)
            api_data = {
                "symbol": "AAPL",
                "data_type": "test",
                "value": 150.50,
                "description": "Manual workflow example",
            }

            # Step 2: Create model instance
            record = ExampleData(**api_data)

            # Step 3: Save to database
            session.add(record)
            await session.commit()
            await session.refresh(record)

            print(f"✅ Saved record: {record}")

        except Exception as e:
            await session.rollback()
            print(f"❌ Error: {e}")
        finally:
            await session.close()
            await engine.dispose()


async def main():
    """Run all examples"""
    print("🚀 Running Worker Examples")
    print("=" * 50)

    # Uncomment the examples you want to run

    # await example_1_simple()
    # await example_2_with_optional_params()
    # await example_3_nested_response()
    await example_4_manual_workflow()

    print("\n" + "=" * 50)
    print("✨ Examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
