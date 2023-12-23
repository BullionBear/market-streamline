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

    async def start(self, on_message: callable):
        await super().start(on_message)

    async def on_depth5(self, base, quote, instrument):
        if instrument.lower() != 'perp':
            raise ValueError(f"instrument allow perp only")
        self.channels += [f'depth5@{base + quote}@{instrument}']
        await self.subscribe(f"{base + quote}@depth5@100ms")

    async def off_depth5(self, base, quote, instrument):
        if instrument.lower() != 'perp':
            raise ValueError(f"instrument allow perp only")
        channel = f'depth5@{base + quote}@{instrument}'
        if channel not in self.channels:
            raise KeyError(f"{base + quote}@{instrument} is not accessible")
        self.channels.remove(channel)
        await self.unsubscribe(f"{base + quote}@depth5@100ms")

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
