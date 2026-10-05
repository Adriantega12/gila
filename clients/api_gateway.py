from clients.base_client import BaseClient
from clients.user_client import UserClient

class ApiGateway:
    def __init__(
        self, 
        base_url: str, 
        auth_token: str = "mysecrettoken",
        env_prefix: str = "dev",
    ):
        self.base_client = BaseClient(
            base_url=base_url, 
            auth_token=auth_token, 
            prefix=env_prefix
        )
        self.user_client = UserClient(self.base_client)