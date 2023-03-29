import databases
import sqlalchemy
import datetime
from CoinModel import CoinIn

DATABASE_URL = "sqlite:///app.db"

class Database():
    def __init__(self) -> None:
        self.connection = databases.Database(DATABASE_URL)
        self.metadata = sqlalchemy.MetaData()

        self.coins = sqlalchemy.Table(
            "coins",
            self.metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("symbol", sqlalchemy.String),
            sqlalchemy.Column("price", sqlalchemy.Float),
            sqlalchemy.Column("datetime", sqlalchemy.DateTime),
        )

        self.engine = sqlalchemy.create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
        self.metadata.create_all(self.engine)

    async def read(self, symbol:str, filter:str):
        if(self.engine.has_table("coins") != True):
            return None
        return await self.connection.fetch_all("SELECT * FROM coins WHERE symbol = '%s' %s LIMIT 24" % (self.translate_currency(symbol), filter))

    def write(self, coin:CoinIn) -> None:
        self.engine.execute("INSERT INTO coins (price, symbol, datetime) VALUES(%s, '%s', '%s')" % (coin.price, self.translate_currency(coin.symbol), datetime.datetime.now()))

    def translate_currency(self, currency_name: str) -> str:
        if currency_name=="bitcoin":
            return "btc"
        elif currency_name=="cardano":
            return "ada"
        elif currency_name=="cosmos":
            return "atom"
        elif currency_name=="ethereum":
            return "eth"
        elif currency_name=="solana":
            return "sol"
        if currency_name=="BTCUSDT":
            return "btc"
        elif currency_name=="ADAUSDT":
            return "ada"
        elif currency_name=="ATOMUSDT":
            return "atom"
        elif currency_name=="ETHUSDT":
            return "eth"
        elif currency_name=="SOLUSDT":
            return "sol"
        else:
            return currency_name