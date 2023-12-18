import asyncio
import unittest
from websocket_manager.okex import OkexClient
from logger import get_logger

logger = get_logger()


class TestOkexClient(unittest.TestCase):
    async def async_test_websocket_connection(self):
        client = OkexClient()
        await client.connect()

        async def callback_func(message):
            print(message)

        await client.subscribe({"channel": "books5", "instId": "BTC-USDT-SWAP"},
                               {"channel": "books5", "instId": "ETH-USDT-SWAP"}
                               )
        await client.start(callback_func)

        # Example duration, modify as needed
        await asyncio.sleep(10)

        await client.unsubscribe({"channel": "books5", "instId": "BTC-USDT-SWAP"})
        await asyncio.sleep(5)
        await client.stop()

    def test_websocket_connection(self):
        asyncio.run(self.async_test_websocket_connection())