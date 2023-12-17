import asyncio
import websockets
import json

from logger import get_logger


class AsyncListenerCore:
    def __init__(self, wss_url):
        self.wss_url = wss_url
        self.connected = False

        self.ws = None
        self.logger = get_logger()
        self.queue = asyncio.Queue()

    async def connect(self):
        try:
            self.ws = await websockets.connect(self.wss_url)
            self.connected = True
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket: {e}")

    async def _attempt_reconnect(self):
        attempt = 0
        while True:
            await asyncio.sleep(5)  # Exponential backoff
            self.logger.warning(f"Attempting to reconnect (Attempt {attempt + 1})")
            await self.connect()
            if self.connected:
                return True

    async def run(self, callback, *args, **kwargs):
        while not self.connected and not await self._attempt_reconnect():
            pass

        websocket_task = asyncio.create_task(self._listen(callback, *args, **kwargs))
        send_task = asyncio.create_task(self._send())
        heartbeat_task = asyncio.create_task(self._heartbeat())
        await asyncio.gather(websocket_task, send_task, heartbeat_task)

    async def _listen(self, callback, *args, **kwargs):
        try:
            while self.connected:
                message = await self.ws.recv()
                message = json.loads(message)
                await callback(message, *args, **kwargs)
        except websockets.ConnectionClosed:
            self.logger.warning("Websocket connection closed")
            self.connected = False
            await self._attempt_reconnect()
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in _listen: {e}")

    async def _send(self):
        while self.connected:
            message = await self.queue.get()
            if message is None:
                break
            try:
                await self.ws.send(message)
                self.logger.info(f"Sent message: {message}")
            except websockets.ConnectionClosed:
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in _send: {e}")

    async def _heartbeat(self):
        while self.connected:
            try:
                await self.ws.ping()
                self.logger.debug("Ping!")
                await asyncio.sleep(30)
            except websockets.ConnectionClosed:
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in _heartbeat: {e}")

    async def send(self, request):
        self.logger.info(f"Putting request to queue: {request}")
        await self.queue.put(json.dumps(request))

    async def disconnect(self):
        if self.connected:
            self.logger.info("Disconnecting Websocket")
            self.connected = False
            await self.ws.close()
            await self.queue.put(None)

    async def is_connected(self):
        return self.connected
