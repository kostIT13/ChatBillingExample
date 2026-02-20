from src.services.auth.userdto import UserDTO
from src.services.auth.base import UserRepository
from typing import Optional


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self._user_repository = {}

    def get_one(self, user_id: str) -> Optional[UserDTO]:
        return self._user_repository.get(user_id)

    def get_all(self, **filters) -> list[UserDTO]:
        all_users = list(self._user_repository.values())
        if not filters:
            return all_users
        else:
            filtered_users = []
            for user in all_users:
                if all(getattr(user, field) == value for field, value in filters.items()):
                    filtered_users.append(user)
            return filtered_users


    def add_one(self, data: UserDTO) -> UserDTO:
        self._user_repository[data.id] = data
        return data