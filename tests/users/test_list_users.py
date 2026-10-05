def test_list_users(api):
    response = api.user_client.list_users()
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
