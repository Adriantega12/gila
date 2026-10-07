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

    get_response = api.user_client.get_user(email)
    assert get_response.status_code == 200

    get_response_body = get_response.json()
    assert get_response_body["email"] == email
    assert get_response_body["name"] == update_payload["name"]
    assert get_response_body["age"] == update_payload["age"]

@pytest.mark.parametrize("age_limit", [1, 150])
def test_update_user_with_age_limits(api, created_user, age_limit):
    email = created_user["email"]
    update_payload = {
        "name": created_user["name"],
        "age": age_limit,
        "email": email,
    }
    put_response = api.user_client.update_user(email, update_payload)
    assert put_response.status_code == 200

    put_body = put_response.json()
    assert put_body["email"] == email
    assert put_body["name"] == update_payload["name"]
    assert put_body["age"] == update_payload["age"]
    
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

    body = response.json()
    assert body["error"] == "User not found"

def test_update_user_to_duplicate_email(api, created_user, create_user_payload):
    payload = create_user_payload(name="William Duplicate")
    create_response = api.user_client.create_user(payload)
    assert create_response.status_code == 201

    try:
        original_email = payload["email"]
        repeated_email = created_user["email"]
        payload["email"] = repeated_email
        put_response = api.user_client.update_user(original_email, payload)
        assert put_response.status_code == 409

        body = put_response.json()
        assert body["error"] == "Email already exists"
    finally:
        api.user_client.delete_user(original_email)

@pytest.mark.parametrize("missing_field", ["name", "email", "age"])
def test_update_user_missing_required_fields(api, created_user, missing_field):
    email = created_user["email"]
    payload = {
        "name": created_user["name"],
        "age": created_user["age"],
        "email": email,
    }
    payload.pop(missing_field)

    response = api.user_client.update_user(email, payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == f"{missing_field} is required"

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    assert body["email"] == email
    assert body["name"] == created_user["name"]
    assert body["age"] == created_user["age"]

def test_update_user_empty_email(api, created_user):
    email = created_user["email"]
    update_payload = {
        "name": created_user["name"],
        "age": created_user["age"],
        "email": "",
    }
    response = api.user_client.update_user(email, update_payload)
    assert response.status_code == 400
    
    body = response.json()
    assert body["error"] == "email is required"

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    assert body["email"] == email
    assert body["name"] == created_user["name"]
    assert body["age"] == created_user["age"]

@pytest.mark.parametrize("invalid_email_format", [
    "itsamerawtext", 
    "@domain",
    "user@",
    # "email withspace@domain.com",
])
def test_update_user_invalid_email_formats(api, created_user, invalid_email_format):
    email = created_user["email"]
    update_payload = {
        "name": created_user["name"],
        "age": created_user["age"],
        "email": invalid_email_format,
    }
    response = api.user_client.update_user(email, update_payload)
    assert response.status_code == 400
    
    body = response.json()
    assert body["error"] == "Invalid email format"

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    assert body["email"] == email
    assert body["name"] == created_user["name"]
    assert body["age"] == created_user["age"]
    
@pytest.mark.parametrize("invalid_age", [-1, 0, 151])
def test_update_user_invalid_age(api, created_user, invalid_age):
    email = created_user["email"]
    name = created_user["name"]
    payload = {
        "name": name,
        "age": invalid_age,
        "email": email,
    }
    response = api.user_client.update_user(email, payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == "Age must be between 1 and 150"

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    assert body["email"] == email
    assert body["name"] == created_user["name"]
    assert body["age"] == created_user["age"]

@pytest.mark.parametrize("invalid_age", ["thisshouldbeanage", 31.416, True, "30"])
def test_update_user_type_mismatch_age(api, created_user, invalid_age):
    email = created_user["email"]
    name = created_user["name"]
    payload = {
        "name": name,
        "age": invalid_age,
        "email": email,
    }
    response = api.user_client.update_user(email, payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == "Age must be between 1 and 150"

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    assert body["email"] == email
    assert body["name"] == created_user["name"]
    assert body["age"] == created_user["age"]