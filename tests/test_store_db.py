import asyncio
import json
from finhub_etl.database import engine
from finhub_etl.utils.save import fetch_and_store_data
from finhub_etl.utils.mappings import HANDLER_MODEL_DICT

async def main():
    # KEY = "recommendation_trends" # done
    # KEY = "market_holiday" # done
    # KEY = "revenue_estimate" # done
    # KEY = "eps_estimate" # done
    # KEY = "ebitda_estimate" # done
    # KEY = "ebit_estimate" # done
    # KEY = "company_profile" # done
    # KEY = "company_profile2" # done
    # KEY = "company_peers" # done
    # KEY = "company_executive" # done
    # KEY = "historical_employee_count" # done
    # KEY = "company_filing" # done
    # KEY = "price_metrics" # done
    # KEY = "historical_market_cap" # done
    # KEY = "earnings_calendar" # done
    # KEY = "basic_financials" # done
    # KEY = "stock_split" # done
    # KEY = "dividend" # done
    # KEY = "general_news" # done
    # KEY = "company_news" # done
    # KEY = "sector_metrics" # done
    # KEY = "market_status" # done
    # KEY = "realtime_quote" # done
    KEY = "candlestick_data"

    # KEY = "press_release" # remain - date null deafult value
    # KEY = "ipo_calendar" # remain - update model
    # KEY = "company_financials" # doubt - 4 statements

    handler = HANDLER_MODEL_DICT[KEY]
    print(handler)


    await fetch_and_store_data(
        handler=handler["handler"],
        model=handler["model"],
        **handler["params"],
    )




if __name__ == "__main__":
    asyncio.run(main())
