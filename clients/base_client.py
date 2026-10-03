# clients/base_client.py
import requests

class BaseClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, **kwargs):
        return self.session.get(self._url(endpoint), **kwargs)

    def post(self, endpoint: str, data=None, json=None, **kwargs):
        return self.session.post(self._url(endpoint), json=json, **kwargs)

    def put(self, endpoint: str, json=None, **kwargs):
        return self.session.put(self._url(endpoint), json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        kwargs.setdefault("timeout")