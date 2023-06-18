from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from app.routes import LoggingRoute
from .histories.views import (
    router as histories_router,
)
from .schemas import (
    GetWalletResponse,
    GetWalletResponseWithHistories,
    GetWalletsResponse,
    PostWalletRequest,
    PostWalletResponse,
    PutWalletRequest,
    PutWalletResponse,
)
from .use_cases import (
    GetWallet,
    ListWallets,
    CreateWallet,
    UpdateWallet,
    DeleteWallet,
)

router = APIRouter(
    prefix="/v1/wallets", route_class=LoggingRoute
)

@router.get("", response_model=GetWalletsResponse)
async def get_wallets(
    use_case: Annotated[
        ListWallets, Depends(ListWallets)
    ]
) -> GetWalletsResponse:
    """Walletの一覧取得API"""
    return GetWalletsResponse(
        wallets=await use_case.execute()
    )

@router.get(
    "/{wallet_id}",
    response_model=GetWalletResponseWithHistories
    | GetWalletResponse,
)
async def get_wallet(
    wallet_id: int,
    use_case: Annotated[
        GetWallet, Depends(GetWallet)
    ],
    include_histories: bool = Query(
        False,
        description="収支項目一覧もレスポンスに含める場合はTrue",
    ),
) -> GetWalletResponseWithHistories | GetWalletResponse:
    """Walletの個別取得API"""
    result = await use_case.execute(
        wallet_id=wallet_id
    )
    if include_histories:
        return (
            GetWalletResponseWithHistories.from_orm(
                result
            )
        )
    return GetWalletResponse.from_orm(result)


@router.post(
    "",
    response_model=PostWalletResponse,
    status_code=status.HTTP_201_CREATED
)
async def post_wallet(
    data: PostWalletRequest,
    use_case: Annotated[
        CreateWallet, Depends(CreateWallet)
    ],
) -> PostWalletResponse:
    """Walletの作成API"""
    return PostWalletResponse.from_orm(
        await use_case.execute(name=data.name)
    )


@router.put(
    "/{wallet_id}",
    response_model=PutWalletResponse
)
async def put_wallet(
    wallet_id: int,
    data: PutWalletRequest,
    use_case: Annotated[
        UpdateWallet, Depends(UpdateWallet)
    ],
) -> PutWalletResponse:
    """Walletの更新API"""
    return PutWalletResponse.from_orm(
        await use_case.execute(
            wallet_id=wallet_id, name=data.name
        )
    )

@router.delete(
    "/{wallet_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wallet(
    wallet_id: int,
    use_case: Annotated[
        DeleteWallet, Depends(DeleteWallet)
    ],
) -> None:
    """Walletの削除API"""
    await use_case.execute(wallet_id=wallet_id)

router.include_router(
    histories_router, prefix="/{wallet_id}"
)
