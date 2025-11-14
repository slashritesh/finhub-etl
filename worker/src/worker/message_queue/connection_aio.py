"""
Async RabbitMQ Connection Manager using aio-pika
"""

import os
from aio_pika import connect_robust, Channel, Connection
from aio_pika.pool import Pool
from dotenv import load_dotenv

load_dotenv()


class AsyncRabbitMQConnection:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.connection: Connection | None = None
        self.channel: Channel | None = None

    async def connect(self) -> Connection:
        """Connect to RabbitMQ using aio-pika."""
        if self.connection and not self.connection.is_closed:
            return self.connection

        print(f"🔌 Connecting to RabbitMQ: {self.url}")

        # Use connect_robust for automatic reconnection
        self.connection = await connect_robust(self.url)

        print("✅ Connected")
        return self.connection

    async def get_channel(self) -> Channel:
        """Return an open channel."""
        if not self.connection or self.connection.is_closed:
            await self.connect()

        if not self.channel or self.channel.is_closed:
            self.channel = await self.connection.channel()
            # Set QoS
            await self.channel.set_qos(prefetch_count=1)

        return self.channel

    async def close(self):
        """Close channel & connection."""
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
            print("📪 Channel closed")

        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("🔌 Connection closed")


# Global instance
async_rabbitmq = AsyncRabbitMQConnection()
