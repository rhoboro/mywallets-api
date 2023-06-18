import pytest

@pytest.mark.anyio
async def test_get_wallets(ac):
    response = await ac.get("/api/v1/wallets")
    assert response.status_code == 200
    assert response.json() == {"wallets": []}
