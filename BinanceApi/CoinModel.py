import datetime
from pydantic import BaseModel

class CoinIn(BaseModel):
    symbol: str
    price: float

class Coin(BaseModel):
    id: int
    symbol: str
    price: float
    datetime: datetime.datetime