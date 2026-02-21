from fastapi import APIRouter, status, Body, Query
from fastapi.responses import JSONResponse
from typing import Optional
from src.api.transaction.schemas import BalanceResponse, TransactionResponse, TopUpRequest, TransactionHistoryQuery
from src.api.auth.dependencies import CurrentUserDependency
from src.api.transaction.dependencies import BillingServiceDependency
from src.api.general_schemas import ErrorResponse, SuccessResponse


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    user: CurrentUserDependency,
    billing_service: BillingServiceDependency
):
    if not user:
        return JSONResponse(
            content=ErrorResponse(message="Требуется авторизация").model_dump(),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    balance = await billing_service.get_current_balance(user.id)
    return BalanceResponse(user_id=user.id, balance=balance)


@router.post("/top-up", response_model=SuccessResponse)
async def top_up_balance(
    user: CurrentUserDependency,
    billing_service: BillingServiceDependency,
    data: TopUpRequest = Body()
):
    if not user:
        return JSONResponse(
            content=ErrorResponse(message="Требуется авторизация").model_dump(),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    await billing_service.create_transaction(
        user_id=user.id, 
        transaction_type="top_up", 
        value=data.value
    )
    
    return JSONResponse(
        content=SuccessResponse(message=f"Баланс пополнен на {data.value} токенов").model_dump(),
        status_code=status.HTTP_201_CREATED
    )


@router.get("/history", response_model=list[TransactionResponse])
async def get_transaction_history(
    user: CurrentUserDependency,
    billing_service: BillingServiceDependency,
    transaction_type: Optional[str] = Query(None),
    limit: int = Query(50, le=100)
):
    if not user:
        return JSONResponse(
            content=ErrorResponse(message="Требуется авторизация").model_dump(),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    filters = {"user_id": user.id}
    if transaction_type:
        filters["transaction_type"] = transaction_type
        
    transactions = await billing_service._transaction_repo.get_all(**filters)
    sorted_trans = sorted(transactions, key=lambda t: t.created_at, reverse=True)[:limit]
    
    return [TransactionResponse.from_dto(t) for t in sorted_trans]