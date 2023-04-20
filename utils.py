import requests
import json
from config import currencies
class ConvertionException(Exception):
    pass

class Convertor():
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Неудается перевести одинаковые валюты {base}.')
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать значение: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currencies[base]]
        return total_base
