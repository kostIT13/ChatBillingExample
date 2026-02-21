from abc import ABC, abstractmethod
from src.services.billing.transactiondto import TransactionDTO
from typing import Literal 


class TransactionRepository(ABC):

    @abstractmethod
    async def get_all(self, **filters) -> list[TransactionDTO]:
        return NotImplemented
    
    @abstractmethod
    async def add_one(self, data: TransactionDTO) -> TransactionDTO:
        return NotImplemented
    
    
class BaseBillingService(ABC):

    @abstractmethod
    async def get_current_balance(self, user_id: str) -> int:
        raise NotImplemented
    
    @abstractmethod
    async def create_transaction(self, user_id: str, transaction_type: Literal["chat", "top_up"], value: int) -> None:
        raise NotImplemented