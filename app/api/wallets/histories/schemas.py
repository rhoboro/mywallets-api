from datetime import datetime
from pydantic import Field, PositiveInt
from app.models import BaseModel, HistoryType
from app.utils.datetime import utcnow

class History(BaseModel):
    history_id: int
    name: str
    amount: PositiveInt
    type: HistoryType = Field(
        ..., description="INCOME:収入, OUTCOME:支出")
    history_at: datetime = Field(
        ..., description="収支項目の発生日時（UTC）")

class GetHistoryResponse(History):
    pass

class GetHistoriesResponse(BaseModel):
    histories: list[History]

class PostHistoryRequest(BaseModel):
    name: str
    amount: PositiveInt
    type: HistoryType = Field(
        ..., description="INCOME:収入, OUTCOME:支出")
    history_at: datetime = Field(
        ..., description="収支項目の発生日時（UTC）")

class PostHistoryResponse(History):
    pass

class PutHistoryRequest(BaseModel):
    name: str
    amount: PositiveInt
    type: HistoryType = Field(
        ..., description="INCOME:収入, OUTCOME:支出")
    history_at: datetime = Field(
        ..., description="収支項目の発生日時（UTC）")

class PutHistoryResponse(History):
    pass

class MoveHistoryRequest(BaseModel):
    destination_id: int = Field(
        ..., description="移動先WalletのID")

class MoveHistoryResponse(History):
    pass
