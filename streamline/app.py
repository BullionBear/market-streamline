from fastapi import FastAPI
from .routers import ws_panel_router

app = FastAPI()

# Include routers
app.include_router(ws_panel_router)