#!/bin/bash

from clients.base_client import BaseClient 

BASE_URL = "http://localhost:3000"

def test_get_users():
    base_client = BaseClient(BASE_URL)
    response = base_client.get("/dev/users")
    assert response.status_code == 200