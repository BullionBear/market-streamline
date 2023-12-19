from fastapi import FastAPI
from .routers import panel_router

app = FastAPI()

# Include routers
app.include_router(panel_router)