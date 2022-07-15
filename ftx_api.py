import time
import hmac

from requests import Request, Response, Session
from typing import Any, List


class FtxApi:
    _URL = 'https://ftx.com/api/'

    def __init__(self, api_key=None, api_secret=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
    
    def _get(self, path: str) -> Any:
        return self._request('GET', path)

    def _request(self, method: str, path: str) -> Any:
        request = Request(method, self._URL + path)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)
    
    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000) # milliseconds
        prepared = request.prepare()
        payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        signature = hmac.new(self._api_secret.encode(), payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)
    
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
    
    def get_all_futures(self) -> List[dict]:
        return self._get('futures')