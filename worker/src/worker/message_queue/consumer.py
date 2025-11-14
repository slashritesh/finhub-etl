"""
Simple RabbitMQ Consumer (pika) - Fully Synchronous
"""

import json
import logging
import asyncio
from .connection import rabbitmq
from worker.utils.save import fetch_and_store_data
from worker.utils.mappings import HANDLER_WITH_SYMBOL

logger = logging.getLogger(__name__)


class TaskConsumer:
    def __init__(self, queue_name: str = "finhub_tasks"):
        self.queue_name = queue_name
        self.channel = None
        self.loop = None

    def process_task(self, data: dict) -> bool:
        """Handle the task logic (synchronous wrapper for async operations)."""
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

            # Run async fetch_and_store_data in the event loop
            self.loop.run_until_complete(
                fetch_and_store_data(
                    handler=handler_func,
                    model=model_class,
                    **params
                )
            )

            logger.info(f"Task {symbol} ({handler_name}) finished successfully")
            return True

        except Exception as e:
            logger.error(f"Error processing task: {e}", exc_info=True)
            return False

    def on_message(self, ch, method, props, body):
        """Handle incoming messages."""
        try:
            data = json.loads(body.decode())
            print(f"Parsed data: {data}")
            logger.info(f"📨 Received task {data.get('symbol', 'unknown')}")

            # Process the task using our dedicated event loop
            ok = self.process_task(data)

            if ok:
                ch.basic_ack(method.delivery_tag)
            else:
                ch.basic_nack(method.delivery_tag, requeue=True)

        except json.JSONDecodeError:
            logger.error("Invalid JSON — dropping message")
            ch.basic_nack(method.delivery_tag, requeue=False)

        except Exception as e:
            logger.error(f"Message error: {e}", exc_info=True)
            ch.basic_nack(method.delivery_tag, requeue=True)

    def start(self):
        """Start consuming messages."""
        # Create a dedicated event loop for async operations
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        try:
            self.channel = rabbitmq.get_channel()

            # Make sure exchange + queue exist
            self.channel.exchange_declare(
                exchange="finhub_exchange", exchange_type="topic", durable=True
            )
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.queue_bind(
                queue=self.queue_name,
                exchange="finhub_exchange",
                routing_key="finhub_tasks"
            )

            logger.info(f"🎧 Listening on queue: {self.queue_name}")
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.on_message,
                auto_ack=False,
            )

            self.channel.start_consuming()

        except KeyboardInterrupt:
            logger.info("🛑 Consumer stopped manually")
            self.stop()

        except Exception as e:
            logger.error(f"Consumer crashed: {e}")
            raise
        finally:
            if self.loop:
                self.loop.close()

    def stop(self):
        """Stop safely."""
        if self.channel:
            self.channel.stop_consuming()
        rabbitmq.close()
        logger.info("👋 Consumer shut down")


# Wrapper for compatibility
def run_consumer(queue_name="finhub_tasks"):
    """Run the consumer synchronously."""
    TaskConsumer(queue_name).start()
