import ftx_api
import pandas as pd

from datetime import datetime as dt

# API key created on 'https://ftx.com/profile'
API_KEY = 'LxIO7YyHJet0bVet36EVNv9ExkxjH3iqjOU9mNqq'
API_SECRET = 'k9_GENAHBzWb8S51MEc1YOXd31ILmaLSe7B_fsqz'

portfolio = ['BTC', 'ETH', 'SOL']
market_type = 'PERP'

epoch = dt(1970, 1, 1, 0, 0, 0)
start = dt(2022, 6, 1, 0, 0, 0)
end = dt(2022, 7, 1, 23, 0, 0)

# start.timestamp() returns GMT +8, not UTC
start_ts = int((start - epoch).total_seconds())
end_ts = int((end - epoch).total_seconds())

hist_data = pd.DataFrame()
api_conn = ftx_api.FtxApi(API_KEY, API_SECRET)
for crypto in portfolio:
    name = f'{crypto}-{market_type}'
    data = api_conn.get_hist_prices(name, 3600, start_ts, end_ts)
    close_price = []
    for hourly_data in data:
        close_price.append(hourly_data['close'])
    hist_data[name] = pd.Series(close_price)

print(hist_data.head())
print(hist_data.tail())
print(len(hist_data))