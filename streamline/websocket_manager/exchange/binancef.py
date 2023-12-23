from .async_client_core import AsyncClientCore
from .interface import Interface


class BinancefClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://fstream.binance.com/ws")
        self.channels = []

    async def get_ws_url(self):
        return self.uri

    async def get_channel(self):
        return self.channels

    async def start(self, message_handler: callable):
        await super().start(message_handler)

    async def subscribe(self, *channels):
        self.channels += channels
        request = {
            "method": "SUBSCRIBE",
            "params": channels,
            "id": 3
        }
        await super().send(request)

    async def unsubscribe(self, *channels):
        for channel in channels:
            self.channels.remove(channel)
        request = {
            "method": "UNSUBSCRIBE",
            "params": channels,
            "id": 2
        }
        await super().send(request)
