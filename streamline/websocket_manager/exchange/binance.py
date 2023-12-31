from streamline.logger import get_logger

from .async_client_core import AsyncClientCore
from .interface import Interface

logger = get_logger()


class BinanceClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://stream.binance.com/ws")
        self.channels = []

    async def get_ws_url(self):
        return self.uri

    async def get_channel(self):
        return self.channels

    async def start(self, on_message: callable):
        await super().start(on_message)

    async def on_diff(self, base, quote, instrument):
        if instrument.lower() != 'spot' or quote.lower() != 'usdt':
            raise ValueError(f"quote allow usdt and instrument allow spot only")
        self.channels += [f'depth@{base + quote}@{instrument}']
        await self.subscribe(f"{base + quote}@depth5@100ms")

    async def off_diff(self, base, quote, instrument):
        if instrument.lower() != 'spot':
            raise ValueError(f"instrument allow spot only")
        channel = f'depth5@{base + quote}@{instrument}'
        if channel not in self.channels:
            raise KeyError(f"{base + quote}@{instrument} is not accessible")
        self.channels.remove(channel)
        await self.unsubscribe(f"{base + quote}@depth@100ms")

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
