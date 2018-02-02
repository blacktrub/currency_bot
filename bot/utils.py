import requests


FIXER_URL = 'https://api.fixer.io/latest'


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
