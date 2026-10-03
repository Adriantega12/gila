from clients.base_client import BaseClient

class UserClient:
    def __init__(self, client: BaseClient):
        self.client = client

    def get_users(self):
        return self.client.get("/dev/users")