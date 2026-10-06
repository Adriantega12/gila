def test_get_user(api, created_user):
    email = created_user["email"]
    response = api.user_client.get_user(email)
    assert response.status_code == 200

    body = response.json()
    assert email == body["email"]
    assert created_user["name"] == body["name"] 
    assert created_user["age"] == body["age"]

def test_get_non_existent_user(api):
    response = api.user_client.get_user("idontexist@world.com")
    assert response.status_code == 404

    body = response.json()
    assert body["error"] == "User not found"