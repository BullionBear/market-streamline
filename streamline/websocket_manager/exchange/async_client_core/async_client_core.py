import asyncio
import websockets
import json

from streamline.logger import get_logger

logger = get_logger()


class AsyncClientCore:
    def __init__(self, uri, max_retries=5, retry_wait=5):
        self.uri = uri
        self.max_retries = max_retries
        self.retry_wait = retry_wait
        self.websocket = None
        self.receiver_task = None
        self.ping_task = None
        self.message_handler = None

    async def __aenter__(self):
        await self.connect_with_retry()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        if self.websocket:
            await self.websocket.close()

    async def connect_with_retry(self):
        retries = 0
        while retries < self.max_retries:
            try:
                await self.connect()
                return
            except (websockets.ConnectionClosedError, OSError) as e:
                retries += 1
                logger.warning(f"Connection failed, retrying ({retries}/{self.max_retries})...")
                await asyncio.sleep(self.retry_wait)

        logger.error("Failed to connect to the WebSocket after retries.")
        raise ConnectionError("Failed to connect to the WebSocket after retries.")

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)

    async def send(self, message):
        await self.websocket.send(json.dumps(message))

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                if self.message_handler:
                    await self.message_handler(message)
        except asyncio.CancelledError:
            logger.info("Message receiving task cancelled")

    async def ping(self):
        try:
            while True:
                await self.websocket.ping()
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            logger.info("Ping task cancelled")

    async def start(self, on_message):
        self.message_handler = on_message
        self.receiver_task = asyncio.create_task(self.receive_messages())
        self.ping_task = asyncio.create_task(self.ping())

    async def stop(self):
        if self.receiver_task:
            self.receiver_task.cancel()
        if self.ping_task:
            self.ping_task.cancel()
        await asyncio.gather(self.receiver_task, self.ping_task, return_exceptions=True)