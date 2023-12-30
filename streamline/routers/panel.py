from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from streamline.websocket_manager import WebsocketManagerFactory, Interface
from streamline.message_handler import PikaHandler
from streamline.logger import get_logger


panel_router = APIRouter()

client: Union[Interface, None] = None

pika_handler: Union[PikaHandler, None] = None

logger = get_logger()


async def message_handler(message):
    logger.debug(message)


async def start_ws_manager(exchange: str):
    global client  # Use the global client variable
    client = WebsocketManagerFactory.create_client(exchange)
    await client.connect()
    await client.start(message_handler)


async def start_pika_handler(exchange_name: str, url: str, username: str, password: str, port: int):
    global pika_handler
    pika_handler = PikaHandler(url, username, password, port)
    await pika_handler.connect(exchange_name)



class StatusResponse(BaseModel):
    ws: str
    channels: list[str]


@panel_router.get("/panel/status", response_model=StatusResponse)
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


@panel_router.post("/panel/on_depth5", response_model=DepthResponse)
async def on_depth5(payload: DepthPayload):
    try:
        await client.on_depth5(payload.base, payload.quote, payload.instrument)
        response = {
            "channels": await client.get_channel()
        }
        return DepthResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@panel_router.post("/panel/off_depth5", response_model=DepthResponse)
async def off_depth5(payload: DepthPayload):
    try:
        await client.off_depth5(payload.base, payload.quote, payload.instrument)
        response = {
            "channels": await client.get_channel()
        }
        return DepthResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))