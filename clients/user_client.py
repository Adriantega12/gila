from typing import Any
from clients.base_client import BaseClient

class UserClient:
    def __init__(self, client: BaseClient):
        self.client = client

    def list_users(self):
        return self.client.get("users")

    def get_user(self, email: str, **kwargs: Any):
        return self.client.get(f"users/{email}", **kwargs)

    def create_user(self, json: dict[str, Any], **kwargs: Any):
        return self.client.post("users", json, **kwargs)

    def update_user(self, email: str, json: dict[str, Any], **kwargs: Any):
        return self.client.put(f"users/{email}", json, **kwargs)

    def delete_user(self, email: str, **kwargs: Any):
        return self.client.delete(f"users/{email}", **kwargs)