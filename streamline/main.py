import uvicorn
from fastapi import FastAPI
from .routers import panel_router, start_panel

app = FastAPI()

# Include routers
app.include_router(panel_router)


@app.on_event("startup")
async def startup_event():
    # Run startup routines for each router
    await start_panel()



