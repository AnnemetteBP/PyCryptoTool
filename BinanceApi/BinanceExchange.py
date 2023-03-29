import time, requests
from threading import Thread
from Interface import Exchange
from CoinModel import CoinIn

class BinanceExchange(Exchange):
    def __init__(self, database, consume_interval:int = 3600):
        super().__init__(database, consume_interval)
        self.key = 'https://api.binance.com/api/v3/ticker/price?symbol='
        self.currencies = ['ATOMUSDT', 'ADAUSDT', 'SOLUSDT', 'ETHUSDT', 'BTCUSDT']
        self.start()

    def stop(self) -> None:
        self.running = False

    def start(self) -> None:        
        thread = Thread(target=self.consume)
        thread.start()

    def consume(self) -> None:
        while(self.running):
            for currency in self.currencies:
                url = self.key+currency
                data = requests.get(url)
                coin = CoinIn(symbol=data.json()['symbol'], price=data.json()['price'])
                self.database.write(coin)
            if (self.running==True):
                time.sleep(self.sleep)
            else:
                print("Thread is skipping sleep")

        print("Thread is stopping")