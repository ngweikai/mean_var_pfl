import ftx_api

# API key created on 'https://ftx.com/profile'
API_KEY = 'LxIO7YyHJet0bVet36EVNv9ExkxjH3iqjOU9mNqq'
API_SECRET = 'k9_GENAHBzWb8S51MEc1YOXd31ILmaLSe7B_fsqz'

api_conn = ftx_api.FtxApi(API_KEY, API_SECRET)
futures = api_conn.get_all_futures()
for key in futures[0].keys():
    print(f'{key}: {futures[0][key]}')