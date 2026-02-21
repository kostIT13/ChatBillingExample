from typing import Optional
from src.services.message.base import MessageRepository
from src.services.message.messagedto import MessageDTO


class InMemoryMessageRepository(MessageRepository):
    _instance: Optional["MessageRepository"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._messages: list[MessageDTO] = []
            self._initialized = True

    async def get_all(self, **filters) -> list[MessageDTO]:
        users = []
        for user in self._messages:
            is_passed = True
            for filter_key, filter_value in filters.items():
                if getattr(user, filter_key) != filter_value:
                    is_passed = False
            if is_passed:
                users.append(user)
        return users

    async def add_one(self, data: MessageDTO) -> MessageDTO:
        self._messages.append(data)
        return data