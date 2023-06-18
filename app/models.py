from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel as _BaseModel
from pydantic import Field, PositiveInt
from app.utils.datetime import to_iso8601

class BaseModel(_BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: to_iso8601,
        }

class Wallet(BaseModel):
    wallet_id: int
    name: str

class HistoryType(StrEnum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"

class History(BaseModel):
    history_id: int
    name: str
    amount: PositiveInt
    type: HistoryType
    history_at: datetime
    wallet_id: int

class Wallet(BaseModel):
    wallet_id: int
    name: str
    histories: list[History]

    @property
    def balance(self) -> int:
        return sum(
            h.amount
            if h.type == HistoryType.INCOME
            else -h.amount
            for h in self.histories
        )
