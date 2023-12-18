from dataclasses import dataclass
from typing import List


@dataclass
class OrderUpdate:
    id: int
    ex: str
    base: str
    quote: str
    inst: str
    ts: int
    u: int
    pu: int
    a: List[float, float]
    b: List[float, float]


