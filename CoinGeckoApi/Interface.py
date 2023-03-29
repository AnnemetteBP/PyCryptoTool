from Database import Database

class Exchange:
    def __init__(self, database:Database, consume_interval:int):
        self.database = database
        self.running = True
        self.sleep = consume_interval

    def consume(self) -> None:
        pass
    def start(self) -> None:
        pass
    def stop(self) -> None:
        pass
    def translate_currency(self, currency_name: str) -> str:
        pass