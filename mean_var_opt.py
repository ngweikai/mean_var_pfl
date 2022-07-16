import ftx_api
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

mean_pct_ret = hist_data.pct_change().mean()
print(mean_pct_ret)
cov_matrix = hist_data.pct_change().cov()

# portfolio simulations
sim_count = 50000
weights = np.zeros((sim_count, len(portfolio)))
returns = np.zeros(sim_count)
risks = np.zeros(sim_count)
sharpe = np.zeros(sim_count)

for i in range(sim_count):
    # create random weights
    w = np.random.random(len(portfolio))
    w = w / np.sum(w)
    weights[i] = w
    # calculate returns
    returns[i] = np.dot(mean_pct_ret, w)
    # calculate risks
    risks[i] = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
    # sharpe ratio
    sharpe[i] = returns[i] / risks[i]

max_index = sharpe.argmax()
print(weights[max_index])

plt.figure(figsize=(16, 10))
plt.scatter(risks, returns, c=sharpe)
plt.xlabel('Portfolio Risk')
plt.ylabel('Portfolio Return')
plt.colorbar(label='Sharpe Ratio')
plt.scatter(risks[max_index], returns[max_index], c='red')
plt.show()