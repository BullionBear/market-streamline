from .async_client_core import AsyncClientCore
from .interface import Interface


class BinanceClient(AsyncClientCore, Interface):
    def __init__(self):
        super().__init__("wss://stream.binance.com/ws")
        self.channels = []

    async def get_ws_url(self):
        return self.uri

    async def get_channel(self):
        return self.channels

    async def start(self, message_handler: callable):
        await super().start(message_handler)

    async def on_depth5(self, base, quote, instrument):
        if instrument.lower() != 'spot' or quote.lower() != 'usdt':
            raise ValueError(f"quote allow usdt and instrument allow spot only")
        self.channels = [('depth5', f'{base + quote}@{instrument}')]
        await self.subscribe(f"{base + quote}@depth5@100ms")

    async def off_depth5(self, base, quote, instrument):
        if instrument.lower() != 'spot' or quote.lower() != 'usdt':
            raise ValueError(f"quote allow usdt and instrument allow spot only")
        self.channels.remove(('depth5', f'{base + quote}@{instrument}'))
        await self.unsubscribe(f"{base + quote}@depth5@100ms")

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
