import uvicorn
from fastapi import FastAPI
from .core.config import settings
from .middleware.auth_middleware import AuthMiddleware
from .routers import ws_panel_router, start_panel

app = FastAPI()

# Include routers
app.include_router(ws_panel_router)
app.add_middleware(AuthMiddleware)


@app.on_event("startup")
async def startup_event():
    # Run startup routines for each router
    pika_url = settings.PIKA_URL
    await start_panel(settings.EXCHANGE, settings.PIKA_EXCHANGE,
                      pika_url.host, pika_url.username, pika_url.password, pika_url.port)
