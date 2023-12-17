import unittest
import asyncio
from websocket_manager.async_listener_core import AsyncListenerCore
import json


class TestAsyncListenerCore(unittest.TestCase):
    def test_listen(self):
        async def test():
            listener = AsyncListenerCore("wss://fstream.binance.com/ws")
            is_connect = await listener.connect()

            # Define a callback function for incoming messages
            def message_handler(message):
                print("Received message:", message)

            if not is_connect:
                return False
            # Run the listener with the callback function
            listener_task = asyncio.create_task(listener.run(message_handler))

            # Send a subscription request
            await asyncio.sleep(1)  # Short delay to ensure the WebSocket connection is established
            await listener.send({
                "method": "SUBSCRIBE",
                "params": ["btcusdt@depth5@100ms"],
                "id": 1
            })

            # Example: Send another subscription request after some time
            await asyncio.sleep(5)
            await listener.send({
                "method": "SUBSCRIBE",
                "params": ["ltcusdt@depth5@100ms"],
                "id": 2
            })

            # Example: Send unsubscription request after some time
            await asyncio.sleep(5)
            await listener.send({
                "method": "UNSUBSCRIBE",
                "params": ["ltcusdt@depth5@100ms"],
                "id": 3
            })

            await asyncio.sleep(5)
            await listener.disconnect()

            # Wait for the listener task or timeout after 30 seconds
            try:
                await asyncio.wait_for(listener_task, 30)
            except asyncio.TimeoutError:
                print("Test timed out after 30 seconds")

        asyncio.run(test())


if __name__ == '__main__':
    unittest.main()