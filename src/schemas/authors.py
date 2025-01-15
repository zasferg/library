from datetime import date
from uuid import UUID
from src.schemas.base import BaseSchema


class AuthorSchema(BaseSchema):
    name: str
    biography: str
    birth_date: date


class GetAuthorSchema(AuthorSchema):
    id: UUID


class CreateAuthorSchema(AuthorSchema):
    pass


class UpdateAuthorSchema(AuthorSchema):
    pass