import asyncio
import unittest
from streamline.websocket_manager import BinanceClient
from streamline.logger import get_logger

logger = get_logger()


class TestBinanceClient(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = BinanceClient()
        await client.connect()

        async def callback_func(message):
            print(message)

        await client.subscribe("btcusdt@depth5@100ms", "ethusdt@depth5@100ms")
        await client.start(callback_func)

        # Example duration, modify as needed
        await asyncio.sleep(10)

        await client.unsubscribe("btcusdt@depth5@100ms")
        await asyncio.sleep(5)
        await client.stop()

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())