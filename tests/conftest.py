from pytest import fixture
from clients.api_gateway import ApiGateway

BASE_URL = "http://localhost:3000"

@fixture(scope="session")
def api() -> ApiGateway:
  return ApiGateway(base_url=BASE_URL)

