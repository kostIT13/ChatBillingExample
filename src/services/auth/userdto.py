from dataclasses import dataclass


@dataclass
class UserDTO:
    id: str
    name: str
    username: str
    hashed_password: str