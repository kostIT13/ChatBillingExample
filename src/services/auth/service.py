import bcrypt
from typing import Optional
from uuid import uuid4
from src.services.auth.base import BaseAuthService, UserRepository
from src.services.auth.userdto import UserDTO


class AuthService(BaseAuthService):


    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def login(self, username: str, password: str) -> Optional[UserDTO]:
        users = await self._user_repository.get_all(username=username)
        for user in users:
            if self._verify_password(password, user.hashed_password):
                return user
        return None

    async def register(self, name: str, username: str, password: str, email: str) -> UserDTO:
        user_id = str(uuid4())

        hashed_password = self._hash_password(password)
        user = UserDTO(
            id=user_id,
            name=name,
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        await self._user_repository.add_one(user)
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[UserDTO]:
        return await self._user_repository.get_one(user_id)

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def _verify_password(password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False