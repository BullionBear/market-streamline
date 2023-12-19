import pydantic
from typing import List, Tuple


class OrderUpdate(pydantic.BaseModel):
    id: int
    ex: str
    base: str
    quote: str
    inst: str
    ts: int
    u: int
    pu: int
    a: List[Tuple[float, float]]
    b: List[Tuple[float, float]]

    @classmethod
    def from_binancef(cls, data: dict):
        symbol = data['s']
        base = symbol[:-4]  # Assuming the last 4 characters are the quote symbol
        quote = symbol[-4:]

        a_list = [(float(price), float(quantity)) for price, quantity in data['a']]
        b_list = [(float(price), float(quantity)) for price, quantity in data['b']]

        return cls(
            id=data['E'],
            ex="binancef",
            base=base,
            quote=quote,
            inst="perp",
            ts=data['T'],
            u=data['u'],
            pu=data['pu'],
            a=a_list,
            b=b_list
        )



