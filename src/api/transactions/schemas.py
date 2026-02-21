from pydantic import BaseModel, Field
from datetime import datetime 
from typing import Literal, Optional, List
from src.services.billing.transactiondto import TransactionDTO


class TopUpRequest(BaseModel):
    value: int = Field(..., gt=0, description="Сумма должна быть больше 0")


class TransactionHistoryQuery(BaseModel):
    limit: int = Field(default=50, le=100)
    transaction_type: Optional[Literal["top_up", "chat", "refund"]] = None


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    transaction_type: str
    value: int
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: TransactionDTO):
        return cls(
            id=dto.id,
            user_id=dto.user_id,
            transaction_type=dto.transaction_type,
            value=dto.value,
            created_at=dto.created_at
        )
    

class BalanceResponse(BaseModel):
    user_id: str
    balance: int
    currency: str = "tokens"