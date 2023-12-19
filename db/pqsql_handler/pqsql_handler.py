import asyncpg
import model

from .const import INSERT_ORDERBOOK, INSERT_DEPTH
class PostgresSQLHandler:
    def __init__(self, username, password, database, host, port):
        self.username = username
        self.password = password
        self.database = database
        self.host = host
        self.port = port

        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(user=self.username, password=self.password,
                                          database=self.database, host=self.host, port=self.port)

    async def insert_order_update(self, order_update: model.OrderUpdate):
        # Insert into orderbook
        await self.conn.execute(INSERT_ORDERBOOK,
                                order_update.id, order_update.ts / 1000, order_update.ex, order_update.inst,
                                order_update.base + order_update.quote)

        # Insert into depth for asks
        for layer, (price, vol) in enumerate(order_update.a):
            await self.conn.execute('''
                INSERT INTO depth(id, layer, side, price, vol) 
                VALUES($1, $2, 'ask', $3, $4)
            ''', order_update.id, layer, price, vol)

        # Insert into depth for bids
        for layer, (price, vol) in enumerate(order_update.b):
            await self.conn.execute('''
                INSERT INTO depth(id, layer, side, price, vol) 
                VALUES($1, $2, 'bid', $3, $4)
            ''', order_update.id, layer, price, vol)
    async def disconnect(self):
        await self.conn.close()
        self.conn = None
