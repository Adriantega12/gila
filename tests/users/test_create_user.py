def test_create_user(api, create_user_payload):
    payload = create_user_payload(name="John Tester")
    response = api.user_client.create_user(payload)
    assert response.status_code == 201

    body = response.json()
    email = body["email"]
    try:
        assert email == payload["email"]
        assert body["name"] == payload["name"]
        assert body["age"] == payload["age"]
    finally:
        api.user_client.delete_user(email)