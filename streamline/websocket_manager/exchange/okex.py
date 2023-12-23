from .async_client_core import AsyncClientCore
from .interface import Interface


class OkexClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://wsaws.okx.com:8443/ws/v5/public")

    async def start(self, message_handler: callable):
        await super().start(message_handler)

    async def subscribe(self, *channels):
        request = {
          "op": "subscribe",
          "args": channels
        }
        await super().send(request)

    async def unsubscribe(self, *channels):
        request = {
          "op": "unsubscribe",
          "args": channels
        }
        await super().send(request)
