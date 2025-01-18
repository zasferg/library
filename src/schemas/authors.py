from datetime import date
from typing import Optional
from uuid import UUID
from src.schemas.base import BaseSchema


class AuthorSchema(BaseSchema):
    name: Optional[str]
    biography: Optional[str]
    birth_date: Optional[date]


class GetAuthorSchema(AuthorSchema):
    id: UUID


class CreateAuthorSchema(AuthorSchema):
    pass


class UpdateAuthorSchema(AuthorSchema):
    pass
