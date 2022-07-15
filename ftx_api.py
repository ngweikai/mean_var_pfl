import time
import hmac

from requests import Request, Response, Session
from typing import Any, Dict, List, Optional


class FtxApi:
    _URL = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
    
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._URL + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)
    
    def _sign_request(self, request: Request) -> None:
        ts_ms = int(time.time()) * 1000 # milliseconds
        prepared = request.prepare()
        payload = f'{ts_ms}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts_ms)
    
    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['Error'])
            return data['result']
    
    def get_markets(self) -> List[dict]:
        return self._get('markets')
    
    def get_market(self, market_name: str = None) -> dict:
        return self._get(f'markets/{market_name}')
    
    def get_hist_prices(
        self, market_name: str, resolution: int = 3600,
        start_time: int = None, end_time: int = None
    ) -> List[dict]:
        return self._get(f'markets/{market_name}/candles', {
            'resolution': resolution,
            'start_time': start_time,
            'end_time': end_time
        })