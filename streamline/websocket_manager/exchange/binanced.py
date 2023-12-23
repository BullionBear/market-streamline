from .async_client_core import AsyncClientCore
from .interface import Interface


class BinancedClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://dstream.binance.com/ws")
        self.channels = []

    async def get_ws_url(self):
        return self.uri

    async def get_channel(self):
        return self.channels

    async def start(self, message_handler: callable):
        await super().start(message_handler)

    async def on_depth5(self, base, quote, instrument):
        if instrument.lower() != 'perp':
            raise ValueError(f"only instrument perp is acceptable")
        self.channels += [f'depth5@{base + quote}_{instrument}@{instrument}']
        await self.subscribe(f"{base + quote}_{instrument}@depth5@100ms")

    async def off_depth5(self, base, quote, instrument):
        if instrument.lower() != 'perp':
            raise ValueError(f"only instrument perp is acceptable")
        channel = f'depth5@{base + quote}@{instrument}'
        if channel not in self.channels:
            raise KeyError(f"{base + quote}@{instrument} is not accessible")
        self.channels.remove(channel)
        await self.unsubscribe(f"{base + quote}_{instrument}@depth5@100ms")

    async def subscribe(self, *channels):
        request = {
            "method": "SUBSCRIBE",
            "params": channels,
            "id": 2
        }
        await super().send(request)

    async def unsubscribe(self, *channels):
        request = {
            "method": "UNSUBSCRIBE",
            "params": channels,
            "id": 2
        }
        await super().send(request)
