import logging
from pytest import fixture
from uuid import uuid4

logger = logging.getLogger(__name__)

@fixture
def create_user_payload():
    def _factory(**overrides):
        payload = {
            "name": "Jane Doe",
            "email": f"user_{uuid4().hex[:8]}@example.com",
            "age": 30,
        }
        payload.update(overrides)
        return payload
    
    return _factory

@fixture
def created_user(api, create_user_payload):
    logger.info("Fixture :: Starting user creation for test:")
    payload = create_user_payload(name = "John Fixture")
    create_response = api.user_client.create_user(payload)
    assert create_response.status_code == 201, (
        f"Fixture setup failed: {create_response.status_code} - {create_response.error}"
    )
    user_data = create_response.json()

    # Hand control to test
    yield user_data

    logger.info("Fixture :: Starting cleanup for test")
    email = user_data["email"]
    delete_response = api.user_client.delete_user(email) 
    assert delete_response.status_code == 204, (f"Fixture teardown :: failed to delete test user {email}: {delete_response.error}")