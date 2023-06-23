from datetime import datetime, timezone
from unittest.mock import ANY

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def setup_data(session: AsyncSession):
    from app.repositories.wallet import WalletORM, HistoryORM
    from app.models import HistoryType

    wallet1 = WalletORM(
        name="foo",
    )
    wallet2 = WalletORM(
        name="bar",
        histories=[
            HistoryORM(
                name="ham",
                amount=1000,
                type=HistoryType.INCOME,
                history_at=datetime(2023, 2, 1, 0, 0, tzinfo=timezone.utc),
            ),
            HistoryORM(
                name="egg",
                amount=300,
                type=HistoryType.OUTCOME,
                history_at=datetime(2023, 2, 1, 1, 0, tzinfo=timezone.utc),
            ),
        ],
    )
    session.add_all([wallet1, wallet2])
    await session.flush()
    await session.commit()


@pytest.mark.anyio
async def test_get_wallets(ac, session: AsyncSession):
    response = await ac.get("/api/v1/wallets")
    assert response.status_code == 200
    assert response.json() == {"wallets": []}


@pytest.mark.anyio
async def test_get_wallets_with_data(ac, session: AsyncSession):
    await setup_data(session)

    response = await ac.get("/api/v1/wallets")
    assert response.status_code == 200
    assert response.json() == {
        "wallets": [
            {"balance": 0, "name": "foo", "wallet_id": ANY},
            {"balance": 700, "name": "bar", "wallet_id": ANY},
        ]
    }


@pytest.mark.anyio
async def test_get_wallet(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(select(WalletORM).where(WalletORM.name == "foo"))

    response = await ac.get(f"/api/v1/wallets/{wallet.wallet_id}")
    assert response.status_code == 200
    assert response.json() == {"balance": 0, "name": "foo", "wallet_id": ANY}


@pytest.mark.anyio
async def test_get_wallet_include_histories(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(select(WalletORM).where(WalletORM.name == "bar"))

    response = await ac.get(
        f"/api/v1/wallets/{wallet.wallet_id}", params={"include_histories": True}
    )
    assert response.status_code == 200
    assert response.json() == {
        "balance": 700,
        "name": "bar",
        "wallet_id": ANY,
        "histories": [
            {
                "history_id": ANY,
                "name": "egg",
                "amount": 300,
                "history_at": "2023-02-01T01:00:00Z",
                "type": "OUTCOME",
            },
            {
                "history_id": ANY,
                "name": "ham",
                "amount": 1000,
                "history_at": "2023-02-01T00:00:00Z",
                "type": "INCOME",
            },
        ],
    }


@pytest.mark.anyio
async def test_post_wallet(ac, session: AsyncSession):
    from app.repositories.wallet import WalletRepository

    await setup_data(session)
    assert len(await WalletRepository().get_all(session)) == 2
    response = await ac.post(
        "/api/v1/wallets",
        json={
            "name": "baz",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"balance": 0, "name": "baz", "wallet_id": ANY}

    wallet = await WalletRepository().get_by_id(session, response.json()["wallet_id"])
    assert wallet.name == "baz"
    assert len(await WalletRepository().get_all(session)) == 3


@pytest.mark.anyio
async def test_put_wallet(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(select(WalletORM).where(WalletORM.name == "foo"))

    response = await ac.put(
        f"/api/v1/wallets/{wallet.wallet_id}",
        json={
            "name": "baz",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "balance": 0,
        "name": "baz",
        "wallet_id": wallet.wallet_id,
    }

    await session.refresh(wallet)
    assert wallet.name == "baz"


@pytest.mark.anyio
async def test_delete_wallet(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM, WalletRepository

    await setup_data(session)
    assert len(await WalletRepository().get_all(session)) == 2
    wallet = await session.scalar(select(WalletORM).where(WalletORM.name == "foo"))
    response = await ac.delete(
        f"/api/v1/wallets/{wallet.wallet_id}",
    )

    assert response.status_code == 204
    assert len(await WalletRepository().get_all(session)) == 1
