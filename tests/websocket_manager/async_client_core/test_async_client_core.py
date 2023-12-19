import asyncio
import unittest
from streamline.websocket_manager.async_client_core import AsyncClientCore
from streamline.logger import get_logger

logger = get_logger()


class TestAsyncClientCore(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = AsyncClientCore("wss://fstream.binance.com/ws")
        await client.connect()
        subscription = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@depth5@100ms", "ethusdt@depth5@100ms"],
            "id": 1
        }

        async def callback_func(message):
            print(message)

        await client.send(subscription)
        await client.start(callback_func)

        # Example duration, modify as needed
        await asyncio.sleep(10)

        unsubscription = {
            "method": "UNSUBSCRIBE",
            "params": ["btcusdt@depth5@100ms"],
            "id": 1
        }

        await client.send(unsubscription)
        await asyncio.sleep(5)
        await client.stop()

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())


if __name__ == "__main__":
    unittest.main()
