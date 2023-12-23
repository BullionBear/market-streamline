from .async_client_core import AsyncClientCore
from .interface import Interface


class BinancedClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://dstream.binance.com/ws")

    async def start(self, message_handler: callable):
        await super().start(message_handler)

    async def subscribe(self, *channels):
        request = {
            "method": "SUBSCRIBE",
            "params": channels,
            "id": 1
        }
        await super().send(request)

    async def unsubscribe(self, *channels):
        request = {
            "method": "UNSUBSCRIBE",
            "params": channels,
            "id": 2
        }
        await super().send(request)
