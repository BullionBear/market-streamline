from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter
from streamline.websocket_manager import WebsocketManagerFactory, Interface

from streamline.logger import get_logger

panel_router = APIRouter()

client: Union[Interface, None] = None

logger = get_logger()


async def message_handler(message):
    print(message)


async def start_panel(exchange: str):
    global client  # Use the global client variable
    client = WebsocketManagerFactory.create_client(exchange)
    await client.connect()
    await client.start(message_handler)


@panel_router.get("/panel/status")
async def get_info():
    return {
        "ws": await client.get_ws_url(),
        "channel": await client.get_channel()
    }


class SubscribePayload(BaseModel):
    base: str
    quote: str


@panel_router.post("/panel/subscribe")
async def subscribe(payload: SubscribePayload):
    channel = f"{(payload.base + payload.quote).lower()}@depth5@100ms"
    await client.subscribe(channel)
    return {"channel": channel}




