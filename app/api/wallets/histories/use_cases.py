from datetime import datetime
from app.models import History, HistoryType
from app.utils.datetime import utcnow

class ListHistories:
    async def execute(
        self, wallet_id: int
    ) -> list[History]:
        return []

class GetHistory:
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        return History(
            wallet_id=wallet_id,
            history_id=history_id,
            name="",
            amount=10,
            type=HistoryType.INCOME,
            history_at=utcnow(),
        )

class CreateHistory:
    async def execute(
        self,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        return History(
            wallet_id=wallet_id,
            history_id=1,
            name=name,
            amount=amount,
            type=type_,
            history_at=history_at,
        )

class UpdateHistory:
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        return History(
            wallet_id=wallet_id,
            history_id=history_id,
            name=name,
            amount=amount,
            type=type_,
            history_at=history_at,
        )

class DeleteHistory:
    async def execute(
        self, wallet_id: int, history_id: int
    ) -> None:
        pass

class MoveHistory:
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        destination_id: int
    ) -> History:
        return History(
            wallet_id=wallet_id,
            history_id=destination_id,
            name="",
            amount=10,
            type=HistoryType.INCOME,
            history_at=utcnow(),
        )
