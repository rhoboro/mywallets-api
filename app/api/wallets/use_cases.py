from app.models import Wallet

class ListWallets:
    async def execute(self) -> list[Wallet]:
        return []

class GetWallet:
    async def execute(
        self, wallet_id: int
    ) -> Wallet:
        return Wallet(
            wallet_id=wallet_id,
            name="",
            histories=[],
        )

class CreateWallet:
    async def execute(
        self, name: str
    ) -> Wallet:
        return Wallet(
            wallet_id=1,
            name=name,
            histories=[],
        )

class UpdateWallet:
    async def execute(
        self, wallet_id: int, name: str
    ) -> Wallet:
        return Wallet(
            wallet_id=wallet_id,
            name=name,
            histories=[],
        )

class DeleteWallet:
    async def execute(
        self, wallet_id: int
    ) -> None:
        pass
