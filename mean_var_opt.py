import ftx_api
import pandas as pd

from datetime import datetime as dt

# API key created on 'https://ftx.com/profile'
API_KEY = 'LxIO7YyHJet0bVet36EVNv9ExkxjH3iqjOU9mNqq'
API_SECRET = 'k9_GENAHBzWb8S51MEc1YOXd31ILmaLSe7B_fsqz'

epoch = dt(1970, 1, 1, 0, 0, 0)
start = dt(2022, 6, 1, 0, 0, 0)
end = dt(2022, 7, 1, 23, 0, 0)

# start.timestamp() returns GMT +8
start_ts = int((start - epoch).total_seconds())
end_ts = int((end - epoch).total_seconds())

time_series = list(range(start_ts, end_ts+1, 3600))
hist_data_df = pd.DataFrame({'timestamp': time_series})

portfolio = ['BTC', 'ETH', 'SOL']
market_type = 'PERP'

api_conn = ftx_api.FtxApi(API_KEY, API_SECRET)
for crypto in portfolio:
    hist_prices = []
    name = f'{crypto}-{market_type}'
    for ts in time_series:
        market = api_conn.get_market_at_ts(name, ts)
        hist_prices.append(float(market['price']))
    hist_data_df[name] = pd.Series(hist_prices)

filepath = 'C:/Users/ngwei/Dropbox/Work/Interview Prep/SingAlliance/mean_var_pfl/portfolio_hist_prices.csv'
try:
    hist_data_df.to_csv(filepath, index=False)
except Exception as e:
    raise e