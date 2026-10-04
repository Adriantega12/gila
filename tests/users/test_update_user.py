def test_update_user(api, created_user):
    email = created_user["email"]
    update_payload = {
        "name": "John Updated",
        "email": email,
        "age": 35,
    }

    # Test update
    put_response = api.user_client.update_user(email, update_payload)
    assert put_response.status_code == 200

    put_body = put_response.json()
    assert put_body["email"] == email
    assert put_body["name"] == update_payload["name"]
    assert put_body["age"] == update_payload["age"]

    # Verify persistence
    get_response = api.user_client.get_user(email)
    assert get_response.status_code == 200

    get_response_body = get_response.json()
    assert get_response_body["email"] == email
    assert get_response_body["name"] == update_payload["name"]
    assert get_response_body["age"] == update_payload["age"]