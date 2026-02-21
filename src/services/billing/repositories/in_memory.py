from typing import Optional
from src.services.billing.transactiondto import TransactionDTO
from src.services.billing.base import TransactionRepository


class InMemoryTransactionRepository(TransactionRepository):
    _instance: Optional["InMemoryTransactionRepository"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._transactions: list[TransactionDTO] = []
            self._initialized = True

    async def get_all(self, **filters) -> list[TransactionDTO]:
        users = []
        for user in self._transactions:
            is_passed = True
            for filter_key, filter_value in filters.items():
                if getattr(user, filter_key) != filter_value:
                    is_passed = False
            if is_passed:
                users.append(user)
        return users

    async def add_one(self, data: TransactionDTO) -> TransactionDTO:
        self._transactions.append(data)
        return data