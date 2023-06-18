from fastapi import APIRouter
from app.routes import LoggingRoute

router = APIRouter(
    prefix="/v1/wallets", route_class=LoggingRoute
)

@router.get("")
async def get_wallets():
    """Walletの一覧取得API"""
    return {"wallets": []}
