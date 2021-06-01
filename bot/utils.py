import decimal
import functools

import requests
import redis


BASE_RATE_API_URL = 'https://www.cbr.ru/Queries/AjaxDataSource/'
RATE_RUB_TO_USD_URL = '{}112805?DT=&val_id=R01235&_=1622572620145'.format(BASE_RATE_API_URL)
RATE_RUB_TO_EUR_URL = '{}112805?DT=&val_id=R01239&_=1622572620146'.format(BASE_RATE_API_URL)
BTC_API_URL = 'https://api.coingecko.com/api/v3/exchange_rates'


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
    def _request(url, attempt=3, **params):
        for _ in range(attempt):
            response = requests.get(url, params=params)
            if response.ok:
                return response.json()

    @staticmethod
    def fmt(val):
        return decimal.Decimal(str(val)).quantize(decimal.Decimal('.00'))

    @cache('usd')
    def rub_to_usd(self):
        data = self._request(
            RATE_RUB_TO_USD_URL
        )
        return data[0]['curs']

    @cache('eur')
    def rub_to_eur(self):
        data = self._request(
            RATE_RUB_TO_EUR_URL
        )
        return data[0]['curs']


class ApiBtc:
    @staticmethod
    def _request(attempts=3):
        for _ in range(attempts):
            response = requests.get(BTC_API_URL)
            if response.ok:
                return response.json()

    @cache('btc')
    def btc_to_usd(self):
        return self._request()['rates']['usd']['value']


currency_api = CurrencyApi()
btc_api = ApiBtc()
