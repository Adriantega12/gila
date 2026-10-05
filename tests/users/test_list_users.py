def test_list_users(api):
    response = api.user_client.list_users()
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)

def test_list_users_with_created_user(api, created_user):
    response = api.user_client.list_users()
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    
    emails = [user["email"] for user in users]
    assert created_user["email"] in emails