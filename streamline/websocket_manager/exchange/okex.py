from .async_client_core import AsyncClientCore
from .interface import Interface


class OkexClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://wsaws.okx.com:8443/ws/v5/public")
        self.channels = []

    async def get_ws_url(self):
        return self.uri

    async def get_channel(self):
        return self.channels

    async def start(self, on_message: callable):
        await super().start(on_message)

    async def on_depth5(self, base, quote, instrument):
        self.channels += [f'depth5@{base + quote}@{instrument}']
        if instrument == 'spot':
            await self.subscribe({"channel": "books5", "instId": f"{base.upper()}-{quote.upper()}"})
        elif instrument == 'perp':
            await self.subscribe({"channel": "books5", "instId": f"{base.upper()}-{quote.upper()}-SWAP"})
        else:
            raise ValueError(f"instrument only support spot and perp")

    async def off_depth5(self, base, quote, instrument):
        channel = f'depth5@{base + quote}@{instrument}'
        if channel not in self.channels:
            raise KeyError(f"{base + quote}@{instrument} is not accessible")
        self.channels.remove(channel)
        await self.unsubscribe(f"{base + quote}@depth5@100ms")

    async def subscribe(self, *channels):
        self.channels += channels
        request = {
          "op": "subscribe",
          "args": channels
        }
        await super().send(request)

    async def unsubscribe(self, *channels):
        for channel in channels:
            self.channels.remove(channel)
        request = {
          "op": "unsubscribe",
          "args": channels
        }
        await super().send(request)
