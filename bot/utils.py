import decimal
import functools

import requests
import redis


RATES_API_URL = 'https://api.ratesapi.io/api/latest'
BTC_API_URL = 'https://blockchain.info/ticker'


def cache(key):
    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            r = redis.StrictRedis()
            value = r.get(key)
            if not value:
                value = func(*args, **kwargs)
                r.set(key, value, ex=60)
            else:
                value = value.decode()

            return value
        return wrapper
    return wrapped


class CurrencyApi:
    @staticmethod
    def _request(attempt=3, **params):
        for _ in range(attempt):
            response = requests.get(RATES_API_URL, params=params)
            if response.ok:
                return response.json()

    @staticmethod
    def fmt(val):
        return decimal.Decimal(str(val)).quantize(decimal.Decimal('.00'))

    @cache('usd')
    def rub_to_usd(self):
        data = self._request(base='USD')
        return self.fmt(data['rates']['RUB'])

    @cache('eur')
    def rub_to_eur(self):
        data = self._request(base='EUR')
        return self.fmt(data['rates']['RUB'])


class ApiBtc:
    @staticmethod
    def _request(attempts=3):
        for _ in range(attempts):
            response = requests.get(BTC_API_URL)
            if response.ok:
                return response.json()

    @cache('btc')
    def btc_to_usd(self):
        return self._request()['USD']['last']


currency_api = CurrencyApi()
btc_api = ApiBtc()
