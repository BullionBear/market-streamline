import asyncio
import unittest
from websocket_manager.async_listener_core import AsyncListenerCore
from logger import get_logger

logger = get_logger()


class TestAsyncListenerCore(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = AsyncListenerCore("wss://fstream.binance.com/ws")
        subscription_request = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth5@100ms"],
            "id": 1
        }

        async def message_handler(message):
            # Process the message here
            logger.info(f"Callback received message: {message}")

        try:
            await client.run(subscription_request, callback=message_handler)
            # Wait for 30 seconds before disconnecting
            await asyncio.sleep(30)
        finally:
            await client.disconnect()

        # Add your assertions here if any

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())


if __name__ == "__main__":
    unittest.main()