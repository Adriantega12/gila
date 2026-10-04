def test_delete_user(api, create_user_payload):
    payload = create_user_payload(name="John Tester")
    response = api.user_client.create_user(payload)
    assert response.status_code == 201

    body = response.json()
    email = body["email"]
    assert email == payload["email"]
    assert body["name"] == payload["name"]
    assert body["age"] == payload["age"]

    delete_response = api.user_client.delete_user(email)
    assert delete_response.status_code == 204

    # Verify Deletion (Crucial assertion)
    get_response = api.user_client.get_user(email)
    assert get_response.status_code == 404