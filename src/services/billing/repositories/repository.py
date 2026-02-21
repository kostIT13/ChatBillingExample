from src.services.billing.base import TransactionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.billing.transactiondto import TransactionDTO
from src.apps.database.models.transactions import Transaction
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from src.apps.database.models.transactions import TransactionType

class SQLAlchemyTransactionRepository(TransactionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session 


    def _to_dto(self, db_trans: Transaction) -> TransactionDTO:
        return TransactionDTO(
            id=db_trans.id,
            user_id=str(db_trans.user_id),
            transaction_type=db_trans.transaction_type,
            value=db_trans.amount,
            created_at=db_trans.created_at
        )
    
    
    async def get_one(self, user_id: str) -> Optional[TransactionDTO]:
        query = select(Transaction).where(Transaction.id==user_id)
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        return self._to_dto(db_user) if db_user else None 
    

    async def get_all(self, **filters) -> List[TransactionDTO]:
        query = select(Transaction)
        if 'user_id' in filters:
            query = query.where(Transaction.user_id == int(filters['user_id']))
        if 'transaction_type' in filters:
            query = query.where(Transaction.transaction_type == filters['transaction_type'])  
        query = query.order_by(desc(Transaction.created_at))
        result = await self.session.execute(query)
        return [self._to_dto(t) for t in result.scalars().all()]  


    async def add_one(self, data: TransactionDTO) -> TransactionDTO:
        db_trans = Transaction(
            id=data.id,
            user_id=data.user_id,
            value=data.value,
            transaction_type=TransactionType(data.transaction_type),
            description=None    
        )
        try:
            self.session.add(db_trans)
            await self.session.commit()
            await self.session.refresh(db_trans)
            return self._to_dto(db_trans)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Ошибка при создании транзакции")