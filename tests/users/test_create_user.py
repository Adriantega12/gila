import pytest

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

def test_create_user_with_duplicate_email(api, create_user_payload, created_user):
    email = created_user["email"]
    payload = create_user_payload(email=email)

    response = api.user_client.create_user(payload)
    assert response.status_code == 409

    body = response.json()
    assert "error" in body # TODO: Correct to right error message check


@pytest.mark.parametrize("missing_field", ["name", "email", "age"])
def test_create_user_missing_required_fields(api, create_user_payload, missing_field):
    payload = create_user_payload()
    payload.pop(missing_field)

    response = api.user_client.create_user(payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == f"{missing_field} is required"

@pytest.mark.parametrize("invalid_email_format", [
    "",
    "thisisnotanemail", 
    "@domain",
    "user@",
])
def test_create_user_invalid_email_formats(api, create_user_payload, invalid_email_format):
    payload = create_user_payload(email=invalid_email_format)

    response = api.user_client.create_user(payload)
    assert response.status_code == 400

    body = response.json()
    assert "error" in body # TODO: Correct to right error message check

@pytest.mark.parametrize("invalid_age", [-1, 0, 151, 31.416])
def test_create_user_invalid_age(api, create_user_payload, invalid_age):
    payload = create_user_payload(age=invalid_age)

    response = api.user_client.create_user(payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == "Age must be between 1 and 150"

def test_create_user_type_mismatch_age(api, create_user_payload):
    payload = create_user_payload(age="thisshouldbeanage")

    response = api.user_client.create_user(payload)
    assert response.status_code == 400

    body = response.json()
    assert body["error"] == "Age must be between 1 and 150"