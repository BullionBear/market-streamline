from fastapi import APIRouter

ws_panel_router = APIRouter()


@ws_panel_router.get("/ws_panel/status")
async def get_status():
    return {"channel": "btcusdt@depth5@100"}