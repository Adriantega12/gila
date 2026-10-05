import os
import logging
from datetime import datetime
from pathlib import Path
from pytest import fixture
from clients.api_gateway import ApiGateway

@fixture(autouse=True)
def per_test_logger(request):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Sanitized test name for filename
    test_name = request.node.name.replace("/", "_").replace(":", "_")
    log_file = log_dir / f"{test_name}.log"

    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)

    yield

    logger.removeHandler(handler)
    handler.close()

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("ENV", "dev"),
        help="Target environment: dev or prod",
    )

@fixture(scope="session")
def env_prefix(request):
    return request.config.getoption("--env")

@fixture(scope="session")
def api(env_prefix) -> ApiGateway:
    base_url = os.getenv("BASE_URL", "http://localhost:3000")
    gateway = ApiGateway(base_url=base_url, env_prefix=env_prefix)
    yield gateway
    gateway.base_client.session.close()
