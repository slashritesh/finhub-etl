"""
Async RabbitMQ Consumer using aio-pika
"""

import json
import logging
from aio_pika import IncomingMessage, ExchangeType
from .connection_aio import async_rabbitmq
from worker.utils.save import fetch_and_store_data
from worker.utils.mappings import HANDLER_WITH_SYMBOL

logger = logging.getLogger(__name__)


class AsyncTaskConsumer:
    def __init__(self, queue_name: str = "finhub_tasks"):
        self.queue_name = queue_name
        self.channel = None
        self.queue = None

    async def process_task(self, data: dict) -> bool:
        """Handle the task logic."""
        try:
            print(f"Process task received data: {data}")
            print(f"Data keys: {data.keys() if isinstance(data, dict) else 'Not a dict!'}")

            symbol = data.get("symbol", "unknown")
            handler_name = data.get("handler")

            print(f"Extracted - Symbol: {symbol}, Handler: {handler_name}")
            logger.info(f"Processing task {symbol} ({handler_name})")

            # Validate handler exists
            if handler_name not in HANDLER_WITH_SYMBOL:
                logger.error(f"Unknown handler: {handler_name}")
                return False

            # Get handler configuration
            handler_config = HANDLER_WITH_SYMBOL[handler_name]
            handler_func = handler_config["handler"]
            model_class = handler_config["model"]

            # Get default params and override with symbol from message
            params = handler_config.get("params", {}).copy()
            params["symbol"] = symbol

            logger.info(f"Calling handler {handler_name} with params: {params}")

            # Fetch and store data
            await fetch_and_store_data(
                handler=handler_func,
                model=model_class,
                **params
            )

            logger.info(f"Task {symbol} ({handler_name}) finished successfully")
            return True

        except Exception as e:
            logger.error(f"Error processing task: {e}", exc_info=True)
            return False

    async def on_message(self, message: IncomingMessage):
        """Handle incoming messages."""
        async with message.process():
            try:
                # Decode and parse JSON
                data = json.loads(message.body.decode())
                print(f"Parsed data: {data}")
                print(f"Data type: {type(data)}")
                logger.info(f"📨 Received task {data.get('symbol', 'unknown')}")

                # Process the task (all async now!)
                ok = await self.process_task(data)

                if not ok:
                    # If processing failed, reject and requeue
                    await message.reject(requeue=True)
                    logger.warning("Task processing failed, requeued")
                # If ok=True, message is automatically acked by the context manager

            except json.JSONDecodeError:
                logger.error("Invalid JSON — dropping message")
                await message.reject(requeue=False)

            except Exception as e:
                logger.error(f"Message error: {e}", exc_info=True)
                await message.reject(requeue=True)

    async def start(self):
        """Start consuming messages."""
        try:
            # Get channel
            self.channel = await async_rabbitmq.get_channel()

            # Declare exchange
            exchange = await self.channel.declare_exchange(
                "finhub_exchange",
                ExchangeType.TOPIC,
                durable=True
            )

            # Declare queue
            self.queue = await self.channel.declare_queue(
                self.queue_name,
                durable=True
            )

            # Bind queue to exchange
            await self.queue.bind(
                exchange="finhub_exchange",
                routing_key="finhub_tasks"
            )

            logger.info(f"🎧 Listening on queue: {self.queue_name}")

            # Start consuming
            await self.queue.consume(self.on_message)

            # Keep the consumer running
            print("Consumer is running. Press Ctrl+C to stop.")

        except Exception as e:
            logger.error(f"Consumer crashed: {e}", exc_info=True)
            raise

    async def stop(self):
        """Stop safely."""
        await async_rabbitmq.close()
        logger.info("👋 Consumer shut down")


async def run_consumer(queue_name="finhub_tasks"):
    """Run the async consumer."""
    consumer = AsyncTaskConsumer(queue_name)
    try:
        await consumer.start()
        # Keep running forever
        import asyncio
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        logger.info("🛑 Consumer stopped manually")
    finally:
        await consumer.stop()
