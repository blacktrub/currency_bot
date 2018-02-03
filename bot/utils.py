import requests


FIXER_URL = 'https://api.fixer.io/latest'
BTC_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'


class ApiFixer:
    @staticmethod
    def _request(attempt=3, **params):
        for _ in range(attempt):
            response = requests.get(FIXER_URL, params=params)
            if response.ok:
                return response.json()

    def rub_to_usd(self):
        data = self._request(base='usd')
        return data['rates']['RUB']

    def rub_to_eur(self):
        data = self._request(base='eur')
        return data['rates']['RUB']


currency_api = ApiFixer()


class ApiBtc:
    @staticmethod
    def _request(attempts=3):
        for _ in range(attempts):
            response = requests.get(BTC_API_URL)
            if response.ok:
                return response.json()

    def btc_to_usd(self):
        data = self._request()
        return [x for x in data if x['id'] == 'bitcoin'][0]['price_usd']


btc_api = ApiBtc()
