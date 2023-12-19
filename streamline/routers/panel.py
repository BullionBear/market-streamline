from fastapi import APIRouter

panel_router = APIRouter()


@panel_router.get("/panel/status")
async def get_status():
    return {"channel": "btcusdt@depth5@100"}