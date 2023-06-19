from collections.abc import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_session
from app.repositories import BaseORM
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, SessionTransaction

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


@pytest.fixture
async def session() -> AsyncGenerator:
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with async_engine.connect() as conn:
        await conn.run_sync(lambda sync_conn: BaseORM.metadata.create_all(sync_conn.engine))

        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()
