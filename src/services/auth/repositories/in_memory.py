from src.services.auth.userdto import UserDTO
from src.services.auth.base import UserRepository
from typing import Optional, List


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self._user_repository: dict[str, UserDTO] = {}

    async def get_one(self, user_id: str) -> Optional[UserDTO]:
        return self._user_repository.get(user_id)

    async def get_all(self, **filters) -> List[UserDTO]:
        all_users = list(self._user_repository.values())
        if not filters:
            return all_users
        
        filtered_users = []
        for user in all_users:
            if all(getattr(user, field, None) == value for field, value in filters.items()):
                filtered_users.append(user)
        return filtered_users

    async def add_one(self,  data: UserDTO) -> UserDTO:
        existing = await self.get_all(username=data.username)
        if existing:
            raise ValueError("Пользователь с таким именем уже существует")
        
        self._user_repository[data.id] = data
        return data