import ftx_api
import pandas as pd

from datetime import datetime as dt

# API key created on 'https://ftx.com/profile'
API_KEY = 'LxIO7YyHJet0bVet36EVNv9ExkxjH3iqjOU9mNqq'
API_SECRET = 'k9_GENAHBzWb8S51MEc1YOXd31ILmaLSe7B_fsqz'

epoch = dt(1970, 1, 1, 0, 0, 0)
start = dt(2022, 6, 1, 0, 0, 0)
end = dt(2022, 7, 1, 23, 0, 0)
now = dt.now()

# start.timestamp() returns GMT +8
start_ts = int((start - epoch).total_seconds())
end_ts = int((end - epoch).total_seconds())

portfolio = ['BTC']
market_type = 'PERP'

api_conn = ftx_api.FtxApi(API_KEY, API_SECRET)
for crypto in portfolio:
    name = f'{crypto}-{market_type}'
    print(name)
    prices = api_conn.get_hist_prices(name)
    market = api_conn.get_market(name)

print(prices[-1])
print(prices[-2])
print(market['price'])