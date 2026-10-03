#!/bin/bash
from clients.base_client import BaseClient
from clients.user_client import UserClient

class ApiGateway:

  def __init__(self, base_url: str):
    self.base_client = BaseClient(base_url=base_url)
    self.user_client = UserClient(self.base_client)