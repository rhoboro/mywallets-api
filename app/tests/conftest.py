import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def ac():
    headers = {"APP-API-KEY": "DUMMY-KEY"}
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers=headers,
    ) as c:
        yield c
