from dataclasses import dataclass
from typing import Optional


@dataclass
class UserDTO:
    id: str
    name: str
    username: str
    hashed_password: str
    email: Optional[str] = None