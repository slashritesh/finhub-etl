# # scheduler_jobs.py

# import logging

# from finhub_etl.loaders.in_universe import get_symbols_list
from finhub_etl.producer.connection import get_producer
# from finhub_etl.utils.mappings import HANDLER_MODEL_DICT


# logger = logging.getLogger(__name__)

# def job_publish_granular_etl():
#     """Publishes 1 message per symbol per handler."""
#     producer = get_producer()
#     symbols = get_symbols_list()

#     print(f"Publishing ETL tasks for {len(symbols)} symbols")
#     logger.info(f"Publishing ETL tasks for {len(symbols)} symbols")

#     for symbol in symbols:
#         for handler_key in HANDLER_MODEL_DICT.keys():

#             message = {
#                 "symbol": symbol,
#                 "handler": handler_key,
#             }
#             print(message)
#             producer.publish(message, routing_key="finhub_tasks")

#     logger.info("All granular ETL tasks published")
#     print(f"Publishing ETL tasks for {len(symbols)} symbols")



producer = get_producer()
message = {
    "symbol": "AAPL",
    "handler": "price_metrics",
}
print(message)
producer.publish(message, routing_key="finhub_tasks")
