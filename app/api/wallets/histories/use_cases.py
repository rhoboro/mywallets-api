from datetime import datetime
from app.database import (
    AsyncSession,
    WalletRepository,
)
from app.exceptions import NotFound
from app.models import History, HistoryType

class ListHistories:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int
    ) -> list[History]:
        async with self.session() as session:
            wallet = await self.repo.get_by_id(
                session, wallet_id
            )
            if not wallet:
                raise NotFound("wallet", wallet_id)

        return wallet.histories

class GetHistory:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        async with self.session() as session:
            history = await self.repo.get_history_by_id(
                session, wallet_id, history_id
            )
            if not history:
                raise NotFound("history", history_id)

        return history

class CreateHistory:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        async with self.session.begin() as session:
            wallet = await self.repo.get_by_id(session, wallet_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)

            history = await self.repo.add_history(
                session,
                wallet.wallet_id,
                name=name,
                amount=amount,
                type_=type_,
                history_at=history_at,
            )
        return history

class UpdateHistory:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        async with self.session.begin() as session:
            history = await self.repo.get_history_by_id(session, wallet_id, history_id)
            if not history:
                raise NotFound("history", history_id)

            history.name = name
            history.amount = amount
            history.type = type_
            history.history_at = history_at
            await self.repo.update_history(session, wallet_id, history)
        return history

class DeleteHistory:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int, history_id: int
    ) -> None:
        async with self.session.begin() as session:
            history = await self.repo.get_history_by_id(session, wallet_id, history_id)
            if history:
                await self.repo.delete_history(session, history.wallet_id, history)

class MoveHistory:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        destination_id: int
    ) -> History:
        async with self.session.begin() as session:
            history = await self.repo.get_history_by_id(session, wallet_id, history_id)
            if not history:
                raise NotFound("history", history_id)

            wallet = await self.repo.get_by_id(session, destination_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)

            history.wallet_id = wallet.wallet_id
            await self.repo.update_history(session, wallet_id, history)
        return history
