import asyncio
import unittest
import asyncpg
import model
from db.pqsql_handler import PostgresSQLHandler  # Replace 'your_module' with the actual module name


class TestPostgresSQLHandler(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.handler = PostgresSQLHandler('bullionbear', 'Sunshine4Jellybean',
                                          'cryptostream', '127.0.0.1', 5432)

    def test_connect_disconnect(self):
        async def test_coroutine():
            await self.handler.connect()
            self.assertIsNotNone(self.handler.conn)
            await self.handler.disconnect()
            self.assertIsNone(self.handler.conn)

        self.loop.run_until_complete(test_coroutine())

    def test_insert_order_update(self):
        async def test_coroutine():
            await self.handler.connect()

            order_update = model.OrderUpdate(
                id=0,
                ex='binance',
                base='btc',
                quote='usdt',
                inst='spot',
                ts=1702952217421,
                u=10,
                pu=0,
                a=[(1.0, 1.0), (2.0, 2.0)],
                b=[(3.0, 1.0)]
            )
            await self.handler.insert_order_update(order_update)
            await self.handler.disconnect()

        self.loop.run_until_complete(test_coroutine())

    def test_insert_order_updates(self):
        async def test_coroutine():
            await self.handler.connect()

            order_update = model.OrderUpdate(
                id=1,
                ex='binance',
                base='btc',
                quote='usdt',
                inst='spot',
                ts=1702952217421,
                u=10,
                pu=0,
                a=[(1.0, 1.0), (2.0, 2.0)],
                b=[(3.0, 1.0)]
            )
            await self.handler.insert_order_updates([order_update])
            await self.handler.disconnect()

        self.loop.run_until_complete(test_coroutine())


if __name__ == '__main__':
    unittest.main()
