from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from streamline.websocket_manager import WebsocketManagerFactory, Interface
from streamline.message_handler import PikaHandler
from streamline.logger import get_logger


ws_panel_router = APIRouter()

client: Union[Interface, None] = None

pika_handler: Union[PikaHandler, None] = None

logger = get_logger()


async def message_handler(message):
    logger.debug(message)


async def start_panel(exchange: str, pika_exchange: str, url: str, username: str, password: str, port: int):
    global client  # Use the global client variable
    client = WebsocketManagerFactory.create_client(exchange)
    await client.connect()

    global pika_handler
    pika_handler = PikaHandler(url, username, password, port)
    await pika_handler.connect(pika_exchange)

    await client.start(message_handler)


class StatusResponse(BaseModel):
    ws: str
    channels: list[str]


@ws_panel_router.get("/panel/status", response_model=StatusResponse)
async def status():
    response = {
        "ws": await client.get_ws_url(),
        "channels": await client.get_channel()
    }
    return StatusResponse(**response)


class DepthPayload(BaseModel):
    base: str
    quote: str
    instrument: str


class DepthResponse(BaseModel):
    channels: list[str]


@ws_panel_router.post("/panel/on_diff", response_model=DepthResponse)
async def on_diff(payload: DepthPayload):
    try:
        await client.on_diff(payload.base, payload.quote, payload.instrument)
        response = {
            "channels": await client.get_channel()
        }
        return DepthResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@ws_panel_router.post("/panel/off_diff", response_model=DepthResponse)
async def off_diff(payload: DepthPayload):
    try:
        await client.off_diff(payload.base, payload.quote, payload.instrument)
        response = {
            "channels": await client.get_channel()
        }
        return DepthResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))