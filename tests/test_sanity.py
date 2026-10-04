def test_list_users(api):
    response = api.user_client.list_users()
    assert response.status_code == 200

def test_create_user(api, create_user_payload):
    payload = create_user_payload(name="John Tester")
    response = api.user_client.create_user(payload)
    assert response.status_code == 201

    body = response.json()
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert body["age"] == payload["age"]

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
 