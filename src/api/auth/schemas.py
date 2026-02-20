from uuid import uuid4
from pydantic import BaseModel, Field
from src.services.auth.userdto import UserDTO
from typing import Optional


class LoginRequest(BaseModel):
    username: str = Field(examples=["admin"])
    password: str = Field(examples=["admin"])


class UserMetadataSchema(BaseModel):
    role: str = Field(default="user", examples=["user"])
    is_verified: bool = Field(default=False, examples=[False])


class LoginResponse(BaseModel):
    id: str = Field(examples=[str(uuid4())])
    display_name: str = Field(examples=["Admin"])
    metadata: UserMetadataSchema 

    @classmethod
    def from_dto(cls, user: UserDTO) -> "LoginResponse":
        return cls(
            id=user.id,
            display_name=user.name,
            metadata=UserMetadataSchema()    
        )
    

class RegisterRequest(BaseModel):
    name: str = Field(examples=["Admin"])
    username: str = Field(examples=["admin"])
    password: str = Field(examples=["admin"])
    email: Optional[str] = Field(default=None, examples=["admin@example.com"])


class UserResponseSchema(BaseModel):
    id: str = Field(examples=[str(uuid4())])
    display_name: str = Field(examples=["Admin"])
    metadata: UserMetadataSchema 

    @classmethod
    def from_dto(cls, user: UserDTO) -> "UserResponseSchema":
        return cls(
            id=user.id,
            display_name=user.name,
            metadata=UserMetadataSchema    
        )
    
    