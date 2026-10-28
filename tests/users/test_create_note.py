import pytest

def test_create_note(api, created_user):
    email = created_user["email"]
    note_content = "A note"
    payload = {
        "note": note_content
    }
    response = api.user_client.create_note(email, payload)
    assert response.status_code == 201

    get_response = api.user_client.get_user(email)
    body = get_response.json()
    
    notes = body["notes"]
    assert len(notes) == 1
    
    note = notes[0]
    assert note == note_content