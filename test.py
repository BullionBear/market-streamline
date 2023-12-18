import asyncio
from websocket_manager.async_listener_core import AsyncListenerCore
from logger import get_logger

logger = get_logger()

async def message_handler(message):
    # Process the message here
    logger.info(f"Callback received message: {message}")

async def main():
    client = AsyncListenerCore("wss://fstream.binance.com/ws")
    subscription_request = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@depth5@100ms"],
        "id": 1
    }

    try:
        await client.run(subscription_request, callback=message_handler)
    finally:
        await client.disconnect()

asyncio.run(main())