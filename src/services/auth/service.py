from typing import Optional
from uuid import uuid4
from passlib.context import CryptContext
from src.services.auth.base import BaseAuthService, UserRepository
from src.services.auth.userdto import UserDTO


class AuthService(BaseAuthService):
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def login(self, username: str, password: str) -> Optional[UserDTO]:
        users = await self._user_repository.get_all(username=username)
        for user in users:
            if self._verify_password(password, user.hashed_password):
                return user
        return None

    async def register(self, name: str, username: str, password: str) -> UserDTO:
        user_id = str(uuid4())
        hashed_password = self._hash_password(password)
        user = UserDTO(
            id=user_id,
            name=name,
            username=username,
            hashed_password=hashed_password
        )
        await self._user_repository.add_one(user)
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        user = await self._user_repository.get_one(user_id)
        return user

    @classmethod
    def _hash_password(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @classmethod
    def _verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(password, hashed_password)