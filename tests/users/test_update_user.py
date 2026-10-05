import pytest

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

def test_update_non_existent_user(api, create_user_payload):
    email = "idontexist@world.com"
    payload = create_user_payload(email=email)
    response = api.user_client.update_user(email, payload)
    assert response.status_code == 404

@pytest.mark.parametrize("missing_field", ["name", "email", "age"])
def test_update_user_missing_required_fields(api, create_user_payload, missing_field):
    payload = create_user_payload()
    email = payload["email"]
    payload.pop(missing_field)
    response = api.user_client.update_user(email, payload)
    assert response.status_code == 400

def test_update_user_type_mismatch_age(api, create_user_payload):
    payload = create_user_payload(age="thisshouldbeanage")
    response = api.user_client.update_user(payload["email"], payload)
    assert response.status_code == 400