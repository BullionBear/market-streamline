import uvicorn
from fastapi import FastAPI
from .core.config import settings
from .middleware.auth_middleware import AuthMiddleware
from .routers import panel_router, start_ws_manager, start_pika_handler

app = FastAPI()

# Include routers
app.include_router(panel_router)
app.add_middleware(AuthMiddleware)


@app.on_event("startup")
async def startup_event():
    # Run startup routines for each router
    await start_ws_manager(settings.EXCHANGE)
    pika_url = settings.PIKA_URL
    await start_pika_handler(settings.PIKA_EXCHANGE,
                             pika_url.host, pika_url.username, pika_url.password, pika_url.port)



