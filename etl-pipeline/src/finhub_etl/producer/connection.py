"""
Simple RabbitMQ Producer
Beginner-friendly clean version using pika.
"""

import os
import json
import pika
from dotenv import load_dotenv

load_dotenv()


class RabbitMQProducer:
    def __init__(
        self,
        url: str | None = None,
        exchange: str = "finhub_exchange",
        exchange_type: str = "topic"
    ):
        # Use env or default URL
        self.url = url or os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.exchange = exchange
        self.exchange_type = exchange_type

        self.connection = None
        self.channel = None

    # -------------------------------------------------------------

    def connect(self):
        """Connect to RabbitMQ"""
        params = pika.URLParameters(self.url)

        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # Create exchange if not exists
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type,
            durable=True
        )

    # -------------------------------------------------------------

    def publish(self, message, routing_key: str):
        """Publish a single message"""
        if not self.channel:
            raise RuntimeError("Not connected. Call connect() first.")

        # Convert dict → JSON
        if isinstance(message, dict):
            message = json.dumps(message)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )

    # -------------------------------------------------------------

    def close(self):
        """Close connection safely"""
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()

    # -------------------------------------------------------------

    # Context manager support
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


# -------------------------------------------------------------
# Helper to get a simple global producer (singleton style)
_producer = None

def get_producer():
    global _producer

    if _producer is None:
        _producer = RabbitMQProducer()
        _producer.connect()

    return _producer
