from pydantic import BaseModel
from fastapi import APIRouter
from streamline.websocket_manager import BinanceClient

from streamline.logger import get_logger

panel_router = APIRouter()

client = BinanceClient()

logger = get_logger()


async def message_handler(message):
    print(message)


async def start_panel():
    await client.connect()
    await client.start(message_handler)


@panel_router.get("/panel/status")
async def get_status():
    return {"channel": "test"}


class SubscribePayload(BaseModel):
    base: str
    quote: str


@panel_router.post("/panel/subscribe")
async def subscribe(payload: SubscribePayload):
    channel = f"{(payload.base + payload.quote).lower()}@depth5@100ms"
    await client.subscribe(channel)
    return {"channel": channel}




