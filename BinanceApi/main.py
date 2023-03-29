from fastapi import FastAPI, Response, status
from typing import List
from CoinModel import Coin
from Database import Database
from BinanceExchange import BinanceExchange
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database()
BinanceExchange(database, 3600)

@app.on_event("startup")
async def startup():
    await database.connection.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.connection.disconnect()

@app.get("/", response_model=List[Coin], status_code=200)
async def read(response: Response, symbol:str, filter:str = ""):
    try:
        data = await database.read(symbol, filter)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        data = List[Coin]()
    return data 