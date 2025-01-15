from uuid import UUID
from pydantic import EmailStr, Field
from src.schemas.base import BaseSchema

class UserSchema(BaseSchema):
    email: EmailStr
    password: str
    is_active: bool = Field(default=True,exclude=True)
    is_superuser: bool = Field(default=False,exclude=True)

class GetUserSchema(UserSchema):
    id: UUID

class CreateUserSchema(UserSchema):
    pass

class UpdateUserSchema(UserSchema):
    pass