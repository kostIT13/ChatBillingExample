from datetime import datetime, timezone
from uuid import uuid4
from typing import Literal
from src.services.billing.transactiondto import TransactionDTO
from src.services.billing.base import BaseBillingService, TransactionRepository

class BillingService(BaseBillingService):
    def __init__(self, transaction_repo: TransactionRepository):
        self._transaction_repo = transaction_repo

    async def get_current_balance(self, user_id: str) -> int:
        transactions = await self._transaction_repo.get_all(user_id=user_id)
        balance = 0
        for t in transactions:
            if t.transaction_type == "top_up":
                balance += t.value
            elif t.transaction_type == "chat":
                balance -= t.value
            elif t.transaction_type == "refund":
                balance += t.value
        return balance

    async def create_transaction(self, user_id: str, transaction_type: Literal["chat", "top_up", "refund"], value: int) -> None:
        if transaction_type == "chat":
            current_balance = await self.get_current_balance(user_id)
            if current_balance < value:
                raise ValueError("Недостаточно средств")
        
        transaction = TransactionDTO(
            id=str(uuid4()),
            user_id=user_id,
            transaction_type=transaction_type,
            value=value,
            created_at=datetime.now(timezone.utc)
        )
        await self._transaction_repo.add_one(transaction)