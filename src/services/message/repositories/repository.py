from src.services.message.base import MessageRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.apps.database.models.message import Message, MessageRole
from src.services.message.messagedto  import MessageDTO
from typing import List
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError


class SQLAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session


    def _to_dto(self, db_msg: Message) -> MessageDTO:
        return MessageDTO(
            id=db_msg.id,
            role=db_msg.role.value,
            text=db_msg.text,
            chat_id=db_msg.chat_id,
            created_at=db_msg.created_at 
        )
    

    async def get_all(self, **filters) -> List[MessageDTO]:
        query = select(Message)
        if 'chat_id' in filters:
            query = query.where(Message.chat_id==filters['chat_id'])
        if 'role' in filters:
            query = query.where(Message.role==MessageRole(filters['role']))
        query = query.order_by(desc(Message.created_at))
        
        result = await self.session.execute(query)
        return [self._to_dto(m) for m in result.scalars().all()]
    
    async def add_one(self, data: MessageDTO) -> MessageDTO:
        db_msg = Message(
            id=data.id,
            chat_id=data.chat_id,
            role=MessageRole(data.role),
            text=data.text    
        )
        try:
            self.session.add(db_msg)
            await self.session.commit()
            await self.session.refresh(db_msg)
            return self._to_dto(db_msg)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Ошибка при создании сообщения")

