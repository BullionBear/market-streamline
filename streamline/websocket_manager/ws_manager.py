from .exchange.binance import BinanceClient
from .exchange.binancef import BinancefClient
from .exchange.binanced import BinancedClient
from .exchange.okex import OkexClient


class WebsocketManagerFactory:
    @staticmethod
    def create_client(exchange: str):
        if exchange == 'binance':
            return BinanceClient()
        elif exchange == 'binancef':
            return BinancefClient()
        elif exchange == 'binanced':
            return BinancedClient()
        elif exchange == 'okex':
            return OkexClient()
        else:
            raise ValueError(f"Unknown exchange: {exchange}")