import asyncio

from db.pqsql_handler import PostgresSQLHandler
from websocket_manager.async_client_core import AsyncClientCore
from websocket_manager import BinancefClient
from logger import get_logger
import model

logger = get_logger()

class Streamline:
    def __init__(self, db_handler):
        self.db_handler: PostgresSQLHandler = db_handler
        self.cluster: dict[str: AsyncClientCore] = {}

        self.queues = [asyncio.Queue(), asyncio.Queue()]  # swap queue algorithm
        self.n_data = 0
    async def connect(self):
        await self.db_handler.connect()

    async def register(self, ex):
        if ex == 'binancef':
            client = BinancefClient()
            await client.start(self.binancef_callback)
        else:
            logger.error(f"{ex} is not implemented")
            raise ValueError(f"{ex} is not implemented")
        self.cluster[ex] = client

    async def subscribe(self, ex: str, base: str, quote: str):
        if ex == 'binancef':
            await self.cluster[ex].subscribe(f'{(base + quote)}@depth5@100ms')
        else:
            logger.error(f"{ex} is not implemented")
            raise ValueError(f"{ex} is not implemented")

    async def binancef_callback(self, message):
        self.n_data += 1
        order_update = model.OrderUpdate.from_binancef(message)
        await self.queues[0].put(order_update)

