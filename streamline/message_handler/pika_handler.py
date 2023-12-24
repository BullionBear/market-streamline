import aio_pika
import pydantic


class PikaHandler:
    def __init__(self, uri, username, password, port=5672):
        self.uri = uri
        self.username = username
        self.password = password
        self.port = port
        self.connection = None
        self.channel = None
        self.exchange = None
        self.routing_key = None

    async def connect(self, exchange_name, routing_key):
        self.connection = await aio_pika.connect_robust(
            host=self.uri,
            port=self.port,
            login=self.username,
            password=self.password
        )

        # Create a channel
        self.channel = await self.connection.channel()

        # Declare the exchange
        self.exchange = await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)

        # Set the routing key
        self.routing_key = routing_key

    async def publish(self, message: pydantic.BaseModel):
        # Serialize the pydantic model to JSON string
        json_message = message.json()

        # Convert the JSON string to bytes
        message_bytes = json_message.encode()

        # Create an aio_pika message
        message = aio_pika.Message(body=message_bytes)

        # Publish the message using the channel, exchange, and routing key
        await self.exchange.publish(message, routing_key=self.routing_key)

