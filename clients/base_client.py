import json
import logging
from typing import Any
from requests import Response, Session

logger = logging.getLogger("api_client")

class BaseClient:
    def __init__(self, base_url: str, auth_token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.session = Session()

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_interaction(self, method: str, url: str, response: Response, **kwargs: Any) -> None:
        log_lines = [
            f"\n{'='*30} HTTP TRANSACTION {'='*30}",
            f"REQ: {method.upper()} {url}",
        ]

        if "headers" in kwargs:
            log_lines.append(f"REQ HEADERS: {kwargs['headers']}")
        if "params" in kwargs:
            log_lines.append(f"REQ PARAMS:  {kwargs['params']}")
        if "json" in kwargs and kwargs["json"] is not None:
            log_lines.append(f"REQ BODY:    {json.dumps(kwargs['json'], indent=2, default=str)}")
        log_lines.append(f"STATUS:       {response.status_code}")
        log_lines.append(f"ELAPSED:      {response.elapsed.total_seconds():.3f}s")

        try:
            resp_json = response.json()
            log_lines.append(
                f"RESP BODY:\n{json.dumps(resp_json, indent=2, default=str)}"
            )
        except Exception:
            log_lines.append(f"RESP BODY (raw):\n{response.text[:1000]}")  # slice to avoid huge binary/HTML dumps

        log_lines.append(f"{'='*78}\n")
        logger.info("\n".join(log_lines))

    def request(self, method: str, endpoint: str, **kwargs: Any) -> Response:
        kwargs.setdefault("timeout", 10)
        url = self._url(endpoint)
        response = self.session.request(method=method, url=url, **kwargs)
        self._log_interaction(method, url, response, **kwargs)
        return response

    def get(self, endpoint: str, **kwargs) -> Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, json=None, **kwargs) -> Response:
        return self.request("POST", endpoint, json=json, **kwargs)

    def put(self, endpoint: str, json=None, **kwargs) -> Response:
        return self.request("PUT", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self.request("DELETE", endpoint, **kwargs)