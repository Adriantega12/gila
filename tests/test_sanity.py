#!/bin/bash

def test_get_users(api):
    response = api.user_client.get_users()
    assert response.status_code == 200