import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
import json
import traceback

from logger import get_logger

logger = get_logger()


class AsyncListenerCore:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.url)
            logger.info("Connected to WebSocket.")
            return True
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            return False

    async def send(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))
            logger.info(f"Sent message: {message}")

    async def receive(self):
        try:
            return await self.websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed.")
            return None

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from WebSocket.")

    async def listen(self, callback):
        while True:
            message = await self.receive()
            if message is None:
                break
            if callback:
                await callback(message)

    async def heartbeat(self):
        while True:
            if self.websocket:
                try:
                    await self.websocket.ping()
                    logger.debug("Sent heartbeat ping.")
                except websockets.exceptions.ConnectionClosed:
                    logger.warning("Heartbeat ping failed, connection closed.")
                    break
            await asyncio.sleep(30)

    async def run(self, subscription_request, callback):
        while not await self.connect():
            logger.warning("Attempting to reconnect...")
            await asyncio.sleep(5)

        await self.send(subscription_request)
        heartbeat_task = asyncio.create_task(self.heartbeat())
        listen_task = asyncio.create_task(self.listen(callback))

        await asyncio.gather(heartbeat_task, listen_task)