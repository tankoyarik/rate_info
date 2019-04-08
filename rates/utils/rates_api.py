from json import JSONDecodeError
from typing import Union

import requests


class RatesApi:
    def __init__(self, url: str='https://api.cryptonator.com/api/ticker/'):
        self.url = url + '{base}-{target}'

    def get_ticker_pair_rate(self, base: str, target: str) -> Union[float, str]:
        '''

        Args:
            base: base currency
            target: target currency

        Returns:
            float price if ok, else string error description
        '''
        url = self.url.format(base=base.lower(),
                              target=target.lower())
        res = requests.get(url)
        try:
            data = res.json()
        except JSONDecodeError as err:
            return err
        if data.get('success'):
            return float(data.get('ticker', {}).get('price'))
        else:
            return data.get('error')


if __name__ == '__main__':
    parser = RatesApi()
    price = parser.get_ticker_pair_rate('BTC', 'USDmm')
    print(price)

#Commit, commit, commit for Yarik