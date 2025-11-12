import asyncio
import json
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT


async def test_handler(key: str, **kwargs):
    """Test a handler and log if it's working."""

    try:
        # Get handler info
        handler_info = HANDLER_MODEL_DICT.get(key)

        if not handler_info:
            print(f"❌ FAILED: Handler key '{key}' not found in mappings")
            return False

        # Get the handler function
        handler_func = handler_info["handler"]
        result = await handler_func(**kwargs)

        print(f"📊 Handler Name : {key}")
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
    TEST_KEY = "historical_market_cap"  # Handler key from mappings

    # Get params from mappings
    handler_info = HANDLER_MODEL_DICT.get(TEST_KEY)
    if not handler_info:
        print(f"❌ Handler key '{TEST_KEY}' not found in mappings")
        return

    # Use params from mappings
    TEST_PARAMS = handler_info.get("params", {})

    print(f"🔧 Testing: {TEST_KEY}")
    print(f"📋 Endpoint: {handler_info.get('endpoint', 'N/A')}")
    print(f"📦 Model: {handler_info.get('model', 'N/A').__name__}")
    print(f"⚙️  Params: {TEST_PARAMS}\n")

    result = await test_handler(TEST_KEY, **TEST_PARAMS)




if __name__ == "__main__":
    asyncio.run(main())
