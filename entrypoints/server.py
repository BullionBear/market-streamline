from fastapi import FastAPI, Request
import time
from streamline.model import RegisterPayload, UnregisterPayload

app = FastAPI()

register_table = {}





@app.post("/api/register")
def register(request: Request, payload: RegisterPayload):
    client_host = request.client.host
    data = dict(payload)
    data.update({"ip": client_host, "timestamp": int(time.time() * 1000)})
    register_table[data['process']] = data
    return {"message": f"Registered {payload.process} successfully"}


@app.post("/api/unregister")
def unregister(payload: UnregisterPayload):
    del register_table[payload.process]
    return {"message": f"Unregistered {payload.process} successfully"}
