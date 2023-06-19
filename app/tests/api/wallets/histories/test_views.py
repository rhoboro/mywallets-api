from datetime import datetime, timezone
from unittest.mock import ANY

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload


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
async def test_get_histories(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(select(WalletORM).where(WalletORM.name == "bar"))

    response = await ac.get(f"/api/v1/wallets/{wallet.wallet_id}/histories")
    assert response.status_code == 200
    assert response.json() == {
        "histories": [
            {
                "history_id": ANY,
                "name": "egg",
                "amount": 300,
                "history_at": "2023-02-01T01:00:00+00:00",
                "type": "OUTCOME",
            },
            {
                "history_id": ANY,
                "name": "ham",
                "amount": 1000,
                "history_at": "2023-02-01T00:00:00+00:00",
                "type": "INCOME",
            },
        ],
    }


@pytest.mark.anyio
async def test_get_history(ac, session: AsyncSession):
    from app.repositories.wallet import HistoryORM

    await setup_data(session)
    history = await session.scalar(
        select(HistoryORM)
        .where(HistoryORM.name == "egg")
        .options(joinedload(HistoryORM.wallet, innerjoin=True))
    )

    response = await ac.get(
        f"/api/v1/wallets/{history.wallet.wallet_id}/histories/{history.history_id}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "history_id": ANY,
        "name": "egg",
        "amount": 300,
        "history_at": "2023-02-01T01:00:00+00:00",
        "type": "OUTCOME",
    }


@pytest.mark.anyio
async def test_post_history(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(
        select(WalletORM)
        .where(WalletORM.name == "bar")
        .options(selectinload(WalletORM.histories))
    )
    assert len(wallet.histories) == 2

    response = await ac.post(
        f"/api/v1/wallets/{wallet.wallet_id}/histories",
        json={
            "name": "spam",
            "amount": 400,
            "history_at": "2023-02-01T02:00:00+00:00",
            "type": "OUTCOME",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "history_id": ANY,
        "name": "spam",
        "amount": 400,
        "history_at": "2023-02-01T02:00:00+00:00",
        "type": "OUTCOME",
    }
    await session.refresh(wallet)
    assert len(wallet.histories) == 3


@pytest.mark.anyio
async def test_put_history(ac, session: AsyncSession):
    from app.repositories.wallet import HistoryORM

    await setup_data(session)
    history = await session.scalar(
        select(HistoryORM)
        .where(HistoryORM.name == "egg")
        .options(joinedload(HistoryORM.wallet, innerjoin=True))
    )

    response = await ac.put(
        f"/api/v1/wallets/{history.wallet.wallet_id}/histories/{history.history_id}",
        json={
            "name": "spam",
            "amount": 600,
            "history_at": "2023-02-01T02:00:00+00:00",
            "type": "OUTCOME",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "history_id": ANY,
        "name": "spam",
        "amount": 600,
        "history_at": "2023-02-01T02:00:00+00:00",
        "type": "OUTCOME",
    }
    await session.refresh(history)
    assert history.name == "spam"
    assert history.amount == 600


@pytest.mark.anyio
async def test_delete_history(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    wallet = await session.scalar(
        select(WalletORM)
        .where(WalletORM.name == "bar")
        .options(selectinload(WalletORM.histories))
    )
    assert len(wallet.histories) == 2

    response = await ac.delete(
        f"/api/v1/wallets/{wallet.wallet_id}/histories/{wallet.histories[0].history_id}",
    )
    assert response.status_code == 204

    await session.refresh(wallet)
    assert len(wallet.histories) == 1


@pytest.mark.anyio
async def test_move_history(ac, session: AsyncSession):
    from app.repositories.wallet import WalletORM

    await setup_data(session)
    foo_wallet = await session.scalar(
        select(WalletORM)
        .where(WalletORM.name == "foo")
        .options(selectinload(WalletORM.histories))
    )
    bar_wallet = await session.scalar(
        select(WalletORM)
        .where(WalletORM.name == "bar")
        .options(selectinload(WalletORM.histories))
    )
    assert len(foo_wallet.histories) == 0
    assert len(bar_wallet.histories) == 2

    history_id = bar_wallet.histories[0].history_id
    response = await ac.post(
        f"/api/v1/wallets/{bar_wallet.wallet_id}/histories/{history_id}/move",
        json={
            "destination_id": foo_wallet.wallet_id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "history_id": history_id,
        "name": "egg",
        "amount": 300,
        "history_at": "2023-02-01T01:00:00+00:00",
        "type": "OUTCOME",
    }
    await session.refresh(foo_wallet)
    await session.refresh(bar_wallet)
    assert len(foo_wallet.histories) == 1
    assert len(bar_wallet.histories) == 1
