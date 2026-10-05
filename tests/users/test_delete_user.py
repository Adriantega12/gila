def test_delete_user(api, create_user_payload):
    payload = create_user_payload(name="John Delete")
    response = api.user_client.create_user(payload)
    assert response.status_code == 201

    body = response.json()
    email = body["email"]
    assert email == payload["email"]
    assert body["name"] == payload["name"]
    assert body["age"] == payload["age"]

    delete_response = api.user_client.delete_user(email)
    assert delete_response.status_code == 204

    # Verify deletion 
    get_response = api.user_client.get_user(email)
    assert get_response.status_code == 404

def test_delete_non_existent_user(api):
    delete_response = api.user_client.delete_user("idontexist@world.com")
    assert delete_response.status_code == 404

def test_delete_user_twice(api, create_user_payload):
    payload = create_user_payload(name="John Delete")
    response = api.user_client.create_user(payload)
    assert response.status_code == 201

    body = response.json()
    email = body["email"]
    assert email == payload["email"]
    assert body["name"] == payload["name"]
    assert body["age"] == payload["age"]

    delete_response = api.user_client.delete_user(email)
    assert delete_response.status_code == 204

    # Confirm it is deleted
    get_response = api.user_client.get_user(email)
    assert get_response.status_code == 404

    # Attempt delete a second time
    delete_response = api.user_client.delete_user(email)
    assert delete_response.status_code == 404