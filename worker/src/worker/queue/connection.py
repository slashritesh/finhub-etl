"""
RabbitMQ Connection Manager

Handles connection lifecycle and channel management for RabbitMQ.
"""

import os
import aio_pika
from typing import Optional
from aio_pika import Connection, Channel, RobustConnection
from aio_pika.abc import AbstractRobustConnection
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConnection:
    """Manages RabbitMQ connection and provides channel access."""

    def __init__(self):
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[Channel] = None
        self.rabbitmq_url = os.getenv(
            "RABBITMQ_URL",
            "amqp://guest:guest@localhost:5672/"
        )

    async def connect(self) -> AbstractRobustConnection:
        """
        Establish connection to RabbitMQ.

        Returns:
            RobustConnection that auto-reconnects on failure
        """
        if self.connection and not self.connection.is_closed:
            return self.connection

        print(f"🔌 Connecting to RabbitMQ: {self.rabbitmq_url}")
        self.connection = await aio_pika.connect_robust(
            self.rabbitmq_url,
            timeout=30,
        )
        print("✅ Connected to RabbitMQ")
        return self.connection

    async def get_channel(self) -> Channel:
        """
        Get or create a channel.

        Returns:
            Active RabbitMQ channel
        """
        if not self.connection:
            await self.connect()

        if not self.channel or self.channel.is_closed:
            self.channel = await self.connection.channel()
            # Enable QoS - process one message at a time
            await self.channel.set_qos(prefetch_count=1)

        return self.channel

    async def close(self):
        """Close channel and connection gracefully."""
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
            print("📪 RabbitMQ channel closed")

        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("🔌 RabbitMQ connection closed")


# Global connection instance
rabbitmq = RabbitMQConnection()
