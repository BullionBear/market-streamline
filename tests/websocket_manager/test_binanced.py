import asyncio
import unittest
from websocket_manager.binanced import BinancedClient
from logger import get_logger

logger = get_logger()


class TestAsyncClientCore(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = BinancedClient()
        await client.connect()

        async def callback_func(message):
            print(message)

        await client.subscribe("btcusd_perp@depth5@100ms")
        await client.start(callback_func)

        # Example duration, modify as needed
        await asyncio.sleep(10)

        await client.unsubscribe("btcusd_perp@depth5@100ms")
        await asyncio.sleep(5)
        await client.stop()

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())