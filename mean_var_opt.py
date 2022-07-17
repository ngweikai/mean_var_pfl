import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime as dt

import ftx_api

# API key created on 'https://ftx.com/profile'
API_KEY = 'LxIO7YyHJet0bVet36EVNv9ExkxjH3iqjOU9mNqq'
API_SECRET = 'k9_GENAHBzWb8S51MEc1YOXd31ILmaLSe7B_fsqz'

# portfolio = ['CEVA', 'GOOGL', 'TSLA', 'ZOM']
portfolio = ['BTC', 'ETH', 'SOL']
market_type = 'PERP'

epoch = dt(1970, 1, 1, 0, 0, 0)
start = dt(2022, 6, 1, 0, 0, 0)
end = dt(2022, 7, 1, 23, 0, 0)

# start.timestamp() returns GMT +8, not UTC
start_ts = int((start - epoch).total_seconds())
end_ts = int((end - epoch).total_seconds())

hist_data = pd.DataFrame()

def get_data_from_yahoo(portfolio: list = None) -> None:
    for stock in portfolio:
        close_data = web.DataReader(stock, 'yahoo', start, end)['Close']
        hist_data[stock] = close_data

def get_data_from_ftx(portfolio: list = None) -> None:
    api_conn = ftx_api.FtxApi(API_KEY, API_SECRET)
    for crypto in portfolio:
        name = f'{crypto}-{market_type}'
        data = api_conn.get_hist_prices(name, 3600, start_ts, end_ts)
        close_price = []
        for hourly_data in data:
            close_price.append(hourly_data['close'])
        hist_data[name] = pd.Series(close_price)

# get_data_from_yahoo(portfolio)
get_data_from_ftx(portfolio)
mean_pct_ret = hist_data.pct_change().mean()
cov_matrix = hist_data.pct_change().cov()

# portfolio simulations
sim_count = 100000
weights = []
returns = []
risks = []
sharpe = []

for _ in range(sim_count):
    # create random weights
    w = np.random.random(len(portfolio))
    w /= w.sum()
    weights.append(w)
    # calculate returns
    ret = np.dot(mean_pct_ret, w)
    returns.append(ret)
    # calculate risks
    risk = np.sqrt(np.dot(w, np.dot(cov_matrix, w.T)))
    risks.append(risk)
    # sharpe ratio
    sharpe.append(ret/risk)

max_index = sharpe.index(max(sharpe))
print(weights[max_index])

plt.figure(figsize=(16, 10))
plt.scatter(risks, returns, c=sharpe)
plt.xlabel('Portfolio Risk')
plt.ylabel('Portfolio Return')
plt.colorbar(label='Sharpe Ratio')
plt.scatter(risks[max_index], returns[max_index], c='red')
plt.show()