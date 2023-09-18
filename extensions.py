import requests
import json

from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Unable to convert identical currencies {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Failed to process currency {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Failed to process currency {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Failed to process quantity {amount}')

        if amount <= 0:
            raise ConvertionException(f'Cannot convert amount of currency less than or equal to 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]*amount

        return total_base
