import asyncio
import unittest
from websocket_manager.async_listener_core import AsyncListenerCore
from logger import get_logger

logger = get_logger()


class TestAsyncListenerCore(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = AsyncListenerCore("wss://fstream.binance.com/ws")
        subscribe_request = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth5@100ms", "ethusdt@depth5@100ms"],
            "id": 1
        }

        async def message_handler(message):
            # Process the message here
            logger.info(f"Callback received message: {message}")

        try:
            await client.run(subscribe_request, callback=message_handler)
            # Wait for 30 seconds before disconnecting
            logger.info("30 seconds passed, attempting to disconnect")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            await client.disconnect()
            logger.info("WebSocket client disconnected")
        # Add your assertions here if any

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())


if __name__ == "__main__":
    unittest.main()