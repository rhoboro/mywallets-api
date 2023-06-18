from pydantic import Field
from app.models import BaseModel
from .histories.schemas import History

class Wallet(BaseModel):
    wallet_id: int
    name: str
    balance: int = Field(
        ..., description="現在時点の予算")

class GetWalletsResponse(BaseModel):
    wallets: list[Wallet]

class GetWalletResponse(Wallet):
    pass

class GetWalletResponseWithHistories(Wallet):
    histories: list[History] = Field(
        ..., description="関連する収支項目一覧")

class PostWalletRequest(BaseModel):
    name: str

class PostWalletResponse(Wallet):
    pass

class PutWalletRequest(BaseModel):
    name: str

class PutWalletResponse(Wallet):
    pass
