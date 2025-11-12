import asyncio
import json
from finhub_etl.database import engine
from finhub_etl.utils.save import fetch_and_store_data
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT

async def main():
    # KEY = "recommendation_trends"
    # KEY = "market_holiday"
    KEY = "eps_estimate"
    handler = HANDLER_MODEL_DICT[KEY]
    print(handler)


    await fetch_and_store_data(
        handler=handler["handler"],
        model=handler["model"],
        **handler["params"],
    )




if __name__ == "__main__":
    asyncio.run(main())
