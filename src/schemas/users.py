from typing import List
from uuid import UUID
from pydantic import EmailStr, Field
from src.schemas.base import BaseSchema
from src.schemas.books import GetBookSchema


class UserSchema(BaseSchema):
    email: EmailStr | None
    password: str | None


class GetUserSchema(UserSchema):
    id: UUID
    is_active: bool = Field(default=True, exclude=True)
    is_superuser: bool = Field(default=False, exclude=True)
    books: List[GetBookSchema] 


class CreateUserSchema(UserSchema):
    pass


class UpdateUserSchema(UserSchema):
    pass
