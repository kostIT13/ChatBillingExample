from abc import ABC, abstractmethod
from src.services.message.messagedto import MessageDTO
from typing import Literal


class MessageRepository(ABC):

    @abstractmethod
    async def get_all(self, **filters) -> list[MessageDTO]:
        raise NotImplemented
    
    @abstractmethod
    async def add_one(self, data: MessageDTO) -> MessageDTO:
        raise NotImplemented
    

class BaseMessageService(ABC):
    @abstractmethod
    async def get_chat_history(self, chat_id: str, size: int = 20) -> list[MessageDTO]:
        raise NotImplemented
    
    @abstractmethod
    async def find_message(self, role: Literal["assistant", "human"], text: str, chat_id: str) -> MessageDTO:
        raise NotImplemented