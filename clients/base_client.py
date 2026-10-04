from requests import Response, Session

class BaseClient:
    def __init__(self, base_url: str, auth_token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.session = Session()

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, **kwargs) -> Response:
        return self.session.get(self._url(endpoint), **kwargs)

    def post(self, endpoint: str, json=None, **kwargs) -> Response:
        return self.session.post(self._url(endpoint), json=json, **kwargs)

    def put(self, endpoint: str, json=None, **kwargs) -> Response:
        return self.session.put(self._url(endpoint), json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.session.delete(self._url(endpoint), **kwargs)