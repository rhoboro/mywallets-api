from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.routes import LoggingRoute
from .schemas import (
    GetHistoriesResponse,
    GetHistoryResponse,
    History,
    MoveHistoryRequest,
    MoveHistoryResponse,
    PostHistoryRequest,
    PostHistoryResponse,
    PutHistoryRequest,
    PutHistoryResponse,
)
from .use_cases import (
    GetHistory,
    ListHistories,
    CreateHistory,
    UpdateHistory,
    DeleteHistory,
    MoveHistory,
)

router = APIRouter(
    prefix="/histories", route_class=LoggingRoute
)

@router.get("", response_model=GetHistoriesResponse)
async def get_histories(
    wallet_id: int,
    use_case: Annotated[
        ListHistories, Depends(ListHistories)
    ],
) -> GetHistoriesResponse:
    """収支項目の一覧取得API"""
    return GetHistoriesResponse(
        histories=[History.model_validate(h)
            for h in await use_case.execute(wallet_id)]
    )

@router.get(
    "/{history_id}",
    response_model=GetHistoryResponse,
)
async def get_history(
    wallet_id: int,
    history_id: int,
    use_case: Annotated[
        GetHistory, Depends(GetHistory)
    ],
) -> GetHistoryResponse:
    """収支項目の個別取得API"""
    return GetHistoryResponse.model_validate(
        await use_case.execute(
            wallet_id=wallet_id,
            history_id=history_id,
        ),
    )

@router.post(
    "",
    response_model=PostHistoryResponse,
    status_code=status.HTTP_201_CREATED
)
async def post_history(
    wallet_id: int,
    data: PostHistoryRequest,
    use_case: Annotated[
        CreateHistory, Depends(CreateHistory)
    ],
) -> PostHistoryResponse:
    """収支項目の作成API"""
    return PostHistoryResponse.model_validate(
        await use_case.execute(
            wallet_id=wallet_id,
            name=data.name,
            amount=data.amount,
            type_=data.type,
            history_at=data.history_at,
        ),
    )


@router.put(
    "/{history_id}",
    response_model=PutHistoryResponse
)
async def put_history(
    wallet_id: int,
    history_id: int,
    data: PutHistoryRequest,
    use_case: Annotated[
        UpdateHistory, Depends(UpdateHistory)
    ],
) -> PutHistoryResponse:
    """収支項目の更新API"""
    return PutHistoryResponse.model_validate(
        await use_case.execute(
            wallet_id=wallet_id,
            history_id=history_id,
            name=data.name,
            amount=data.amount,
            type_=data.type,
            history_at=data.history_at,
        ),
    )


@router.delete(
    "/{history_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_history(
    wallet_id: int,
    history_id: int,
    use_case: Annotated[
        DeleteHistory, Depends(DeleteHistory)
    ],
) -> None:
    """収支項目の削除API"""
    await use_case.execute(
        wallet_id=wallet_id, history_id=history_id)


@router.post(
    "/{history_id}/move",
    response_model=MoveHistoryResponse,
    description="",
)
async def move_history(
    wallet_id: int,
    history_id: int,
    data: MoveHistoryRequest,
    use_case: Annotated[
        MoveHistory, Depends(MoveHistory)
    ],
) -> MoveHistoryResponse:
    """収支項目の移動API

    収支項目を指定したWalletに移動する
    移動成功後は元の場所へのリクエストは404になる
    """
    return MoveHistoryResponse.model_validate(
        await use_case.execute(
            wallet_id=wallet_id,
            history_id=history_id,
            destination_id=data.destination_id,
        ),
    )
