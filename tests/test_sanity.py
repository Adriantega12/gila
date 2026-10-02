#!/bin/bash

import requests

BASE_URL = "http://localhost:3000"

def test_get_users():
    response = requests.get(f"{BASE_URL}/dev/users")
    assert response.status_code == 200