import asyncpg
import model
from datetime import datetime
from .const import INSERT_ORDER_UPDATE


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
        # Convert the timestamp from milliseconds to a datetime object
        ts_datetime = datetime.utcfromtimestamp(order_update.ts / 1000.0)

        # Prepare data for 'a' and 'b' columns
        a_prices, a_sizes = zip(*order_update.a) if order_update.a else ([], [])
        b_prices, b_sizes = zip(*order_update.b) if order_update.b else ([], [])

        # Insert data into the table
        await self.conn.execute(INSERT_ORDER_UPDATE, order_update.id, order_update.ex, order_update.base, order_update.quote,
                                order_update.inst, ts_datetime, order_update.u, order_update.pu,
                                a_prices, a_sizes, b_prices, b_sizes)

    async def insert_order_updates(self, order_updates: list[model.OrderUpdate]):
        # Prepare the data for insertion
        values = [
            (
                order_update.id, order_update.ex, order_update.base, order_update.quote,
                order_update.inst, datetime.utcfromtimestamp(order_update.ts / 1000.0),
                order_update.u, order_update.pu,
                [price for price, _ in order_update.a],
                [size for _, size in order_update.a],
                [price for price, _ in order_update.b],
                [size for _, size in order_update.b]
            )
            for order_update in order_updates
        ]

        # Execute the batch insert
        await self.conn.executemany(INSERT_ORDER_UPDATE, values)

    async def disconnect(self):
        await self.conn.close()
        self.conn = None
