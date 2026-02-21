from src.services.auth.base import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from src.services.auth.userdto import UserDTO
from src.apps.database.models.user import User
from sqlalchemy.exc import IntegrityError


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_dto(self, db_user: User) -> UserDTO:
        return UserDTO(
            id=str(db_user.id),
            name=db_user.name,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.password_hash
        )

    async def get_one(self, user_id: str) -> Optional[UserDTO]:
        query = select(User).where(User.id==user_id)
        result = await self.session.execute(query)
        db_user = result.scalar_one_or_none()
        return self._to_dto(db_user) if db_user else None 
    
    async def get_all(self, **filters) -> List[UserDTO]:
        query = select(User)
        for field, value in filters.items():
            if hasattr(User, field):
                query = query.where(getattr(User, field) == value)

        result = await self.session.execute(query)
        return [self._to_dto(u) for u in result.scalars().all()]
    
    async def add_one(self, data: UserDTO) -> UserDTO:
        db_user = User(
            id=data.id,
            name=data.name,
            username=data.username,
            email=data.email,
            password_hash=data.hashed_password
        )
        try:
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return self._to_dto(db_user)
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError("Пользователь уже существует")
        
