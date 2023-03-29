import time
from threading import Thread
from pycoingecko import CoinGeckoAPI
from Interface import Exchange
from CoinModel import CoinIn

class CoinGeckoExchange(Exchange):
    def __init__(self, database, consume_interval:int = 3600):
        super().__init__(database, consume_interval)
        self.cg = CoinGeckoAPI()
        self.currencies = ['cosmos', 'cardano', 'solana', 'ethereum', 'bitcoin']
        self.start()

    def stop(self) -> None:
        self.running = False

    def start(self) -> None:        
        thread = Thread(target=self.consume)
        thread.start()

    def consume(self) -> None:
        currency_standard = 'usd'
        while(self.running):
            data = self.cg.get_price(ids=self.currencies, vs_currencies=currency_standard)
            for currency in self.currencies:
                coin = CoinIn(symbol=currency, price=data[currency][currency_standard])
                self.database.write(coin)
            if (self.running==True):
                time.sleep(self.sleep)
            else:
                print("Thread is skipping sleep")

        print("Thread is stopping")