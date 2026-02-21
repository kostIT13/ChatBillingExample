from datetime import datetime 
from uuid import uuid4
from src.services.message.messagedto import MessageDTO
from src.services.message.base import BaseMessageService, MessageRepository
from typing import Literal


class MessageService(BaseMessageService):
    def __init__(self, message_repo: MessageRepository):
        self._message_repo = message_repo

    async def get_chat_history(self, chat_id: str, size: int = 20) -> list[MessageDTO]:
        messages = await self._message_repo.get_all(chat_id=chat_id)
        sorted_messages = sorted(messages, key=lambda m: m.created_at)
        return sorted_messages[-size:]

    async def create_message(self, role: Literal["assistant", "human"], text: str, chat_id: str) -> MessageDTO:
        message_id = str(uuid4())
        created_at = datetime.datetime.now()
        message = MessageDTO(
            id=message_id,
            role=role,
            text=text,
            chat_id=chat_id,
            created_at=created_at
        )
        created_message = await self._message_repo.add_one(message)
        return created_message