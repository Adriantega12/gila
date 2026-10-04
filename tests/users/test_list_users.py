def test_list_users(api):
    response = api.user_client.list_users()
    assert response.status_code == 200
    body = response.json()
    # Depending on whether your API returns a raw list [...] or a paginated dict {"items": [...]}
    assert isinstance(body, list)
 