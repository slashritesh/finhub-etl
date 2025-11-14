"""
Simple RabbitMQ Connection Manager using pika (Beginner Friendly)
"""

import os
import pika
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConnection:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.connection = None
        self.channel = None

    # -------------------------------------------------------------

    def connect(self):
        """Connect to RabbitMQ using pika."""
        if self.connection and self.connection.is_open:
            return self.connection

        print(f"🔌 Connecting to RabbitMQ: {self.url}")

        params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # Basic QoS
        self.channel.basic_qos(prefetch_count=1)

        print("✅ Connected")
        return self.connection

    # -------------------------------------------------------------

    def get_channel(self):
        """Return an open channel."""
        if not self.connection or self.connection.is_closed:
            self.connect()

        if not self.channel or self.channel.is_closed:
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)

        return self.channel

    # -------------------------------------------------------------

    def close(self):
        """Close channel & connection."""
        if self.channel and self.channel.is_open:
            self.channel.close()
            print("📪 Channel closed")

        if self.connection and self.connection.is_open:
            self.connection.close()
            print("🔌 Connection closed")


# Global instance
rabbitmq = RabbitMQConnection()
