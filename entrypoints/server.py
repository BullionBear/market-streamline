from fastapi import FastAPI, Request
import time
import pydantic

app = FastAPI()

register_table = {}


class RegisterPayload(pydantic.BaseModel):
    exchange: str
    quote: str
    base: str
    instrument: str
    channel: str
    type: str  # rest or ws
    process: int


@app.post("/api/register")
def register(request: Request, payload: RegisterPayload):
    client_host = request.client.host
    data = dict(payload)
    data.update({"ip": client_host, "timestamp": int(time.time() * 1000)})
    register_table[data['process']] = data
    return {"message": f"Registered {payload.process} successfully"}


class UnregisterPayload(pydantic.BaseModel):
    process: int


@app.post("/api/unregister")
def unregister(payload: UnregisterPayload):
    del register_table[payload.process]
    return {"message": f"Unregistered {payload.process} successfully"}
