from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from app.models import HistoryType
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.exceptions import AppException
from app.models import History, Wallet

class BaseORM(DeclarativeBase):
    pass

class HistoryORM(BaseORM):
    __tablename__ = "histories"
    history_id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str]
    amount: Mapped[int] = mapped_column(
        Integer, CheckConstraint("amount > 0")
    )
    type: Mapped[HistoryType] = mapped_column(
        Enum(HistoryType)
    )
    wallet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "wallets.wallet_id", ondelete="CASCADE"
        ),
        index=True,
    )
    history_at: Mapped[datetime]
    wallet: Mapped["WalletORM"] = relationship(
        back_populates="histories"
    )

    @classmethod
    def from_entity(cls, history: History):
        return cls(
            history_id=history.history_id,
            name=history.name,
            amount=history.amount,
            type=history.type,
            wallet_id=history.wallet_id,
            history_at=history.history_at,
        )

    def to_entity(self) -> History:
        return History.from_orm(self)

    def update(self, history: History) -> None:
        self.name = history.name
        self.amount = history.amount
        self.type = history.type
        self.wallet_id = history.wallet_id
        self.history_at = history.history_at

class WalletORM(BaseORM):
    __tablename__ = "wallets"
    wallet_id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str]
    histories: Mapped[
        list[HistoryORM]
    ] = relationship(
        back_populates="wallet",
        order_by=HistoryORM.history_at.desc(),
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )

    @classmethod
    def from_entity(cls, wallet: Wallet):
        return cls(
            wallet_id=wallet.wallet_id,
            name=wallet.name,
            histories=wallet.histories,
        )

    def to_entity(self) -> Wallet:
        return Wallet.from_orm(self)

    def update(self, wallet: Wallet, histories: list[HistoryORM]) -> None:
        self.name = wallet.name
        self.histories = histories

class WalletRepository:
    async def add(
        self, session: AsyncSession, name: str
    ) -> Wallet:
        wallet = WalletORM(name=name, histories=[])
        session.add(wallet)
        await session.flush()
        return wallet.to_entity()

    async def get_by_id(
        self,
        session: AsyncSession,
        wallet_id: int,
    ) -> Wallet | None:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            )
        )
        wallet = await session.scalar(stmt)
        if not wallet:
            return None
        return wallet.to_entity()

    async def get_all(
        self, session: AsyncSession
    ) -> list[Wallet]:
        stmt = select(WalletORM).options(
            selectinload(WalletORM.histories)
        )
        return [
            wallet.to_entity()
            for wallet in await session.scalars(
                stmt
            )
        ]

    async def add_history(
        self,
        session: AsyncSession,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            )
        )
        wallet = await session.scalar(stmt)
        if not wallet:
            raise AppException()

        history = HistoryORM(
            name=name,
            amount=amount,
            type=type_,
            history_at=history_at,
            wallet_id=wallet.wallet_id,
        )
        wallet.histories.append(history)
        await session.flush()
        return history.to_entity()

    async def update(self, session: AsyncSession, wallet: Wallet) -> Wallet:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet.wallet_id)
            .options(selectinload(WalletORM.histories))
        )
        wallet_ = await session.scalar(stmt)
        if not wallet_:
            raise AppException()

        wallet_.update(wallet, wallet_.histories)
        await session.flush()
        return wallet_.to_entity()

    async def delete(self, session: AsyncSession, wallet: Wallet) -> None:
        stmt = select(WalletORM).where(WalletORM.wallet_id == wallet.wallet_id)
        wallet_ = await session.scalar(stmt)
        if wallet_:
            await session.delete(wallet_)

    async def get_history_by_id(
        self,
        session: AsyncSession,
        wallet_id: int,
        history_id: int,
    ) -> History | None:
        stmt = (
            select(HistoryORM)
            .where(
                HistoryORM.wallet_id == wallet_id, HistoryORM.history_id == history_id
            )
            .options(joinedload(HistoryORM.wallet))
        )
        history_ = await session.scalar(stmt)
        if not history_:
            return None

        return history_.to_entity()

    async def update_history(
        self, session: AsyncSession, wallet_id: int, history: History
    ) -> History:
        stmt = select(HistoryORM).where(
            HistoryORM.wallet_id == wallet_id,
            HistoryORM.history_id == history.history_id,
            )
        history_ = await session.scalar(stmt)
        if not history_:
            raise AppException()

        history_.update(history)
        await session.flush()
        return history_.to_entity()

    async def delete_history(
        self, session: AsyncSession, wallet_id: int, history: History
    ):
        stmt = select(HistoryORM).where(
            HistoryORM.wallet_id == wallet_id,
            HistoryORM.history_id == history.history_id,
            )
        history_ = await session.scalar(stmt)
        if history_:
            await session.delete(history_)
