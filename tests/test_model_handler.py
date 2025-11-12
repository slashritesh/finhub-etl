import asyncio
import json
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT


async def test_handler(key: str, **kwargs):
    """Test a handler and log if it's working."""
   
    print(f"Testing: {key}")
    print(f"{'='*60}")

    try:
        # Get handler info
        handler_info = HANDLER_MODEL_DICT.get(key)

        if not handler_info:
            print(f"❌ FAILED: Handler key '{key}' not found in mappings")
            return False

        # Get the handler function
        handler_func = handler_info["handler"]
        

       
        # Call the handler
        result = await handler_func(**kwargs)

        # Log success
        print("\n✅ SUCCESS: Handler responded")
        print(f"📊 Response type: {type(result).__name__}")

        # Pretty print result (truncated)
        result_str = json.dumps(result, indent=2, default=str)
        if len(result_str) > 500:
            result_str = result_str[:500] + "\n... (truncated)"
        print(f"\n📄 Response:\n{result_str}")

        return True

    except Exception as e:
        print(f"\n❌ FAILED: {type(e).__name__}")
        print(f"Error: {str(e)}")
        return False


async def main():
    # Test configuration
    TEST_KEY = "recommendation_trends"  # Handler key from mappings
    TEST_PARAMS = {
        "symbol": "AAPL"  # Test symbol
    }

    # Run test
    success = await test_handler(TEST_KEY, **TEST_PARAMS)

    # Summary
    print(f"\n{'='*60}")
    if success:
        print("✅ Test completed successfully")
    else:
        print("❌ Test failed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
