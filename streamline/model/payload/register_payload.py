import pydantic


class RegisterPayload(pydantic.BaseModel):
    exchange: str
    quote: str
    base: str
    instrument: str
    channel: str
    type: str  # rest or ws
    process: int


class UnregisterPayload(pydantic.BaseModel):
    process: int
