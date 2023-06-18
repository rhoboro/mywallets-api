import logging
from typing import Annotated, AsyncIterator
from fastapi import Depends
from sqlalchemy import Connection, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from app.exceptions import AppException
from app.repositories import BaseORM
from app.repositories import (
    WalletRepository as _WalletRepository,
)

logger = logging.getLogger(__name__)
async_engine = create_async_engine(
    "sqlite+aiosqlite:///database.db",
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
)

async def get_session() -> AsyncIterator[
    async_sessionmaker
]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
        raise AppException() from e

AsyncSession = Annotated[
    async_sessionmaker, Depends(get_session)
]

WalletRepository = Annotated[
    _WalletRepository, Depends(_WalletRepository)
]

async def create_database_if_not_exist() -> None:

    def create_tables_if_not_exist(
        sync_conn: Connection,
    ) -> None:
        if not inspect(sync_conn.engine).has_table(
            "wallets"
        ):
            BaseORM.metadata.create_all(
                sync_conn.engine
            )

    async with async_engine.connect() as conn:
        await conn.run_sync(
            create_tables_if_not_exist
        )
