from clients.base_client import BaseClient
from clients.user_client import UserClient

class ApiGateway:
    def __init__(
        self, 
        base_url: str, 
        auth_token: str | None = None,
        env_prefix: str = "dev",
    ):
        self.base_client = BaseClient(
            base_url=base_url, 
            auth_token=auth_token, 
            prefix=env_prefix
        )
        self.base_client_prod = BaseClient(
            base_url=base_url, 
            auth_token=auth_token, 
            prefix="prod",
        )
        self.user_client = UserClient(self.base_client)
        self.user_client_prod = UserClient(self.base_client_prod)