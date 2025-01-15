from uuid import UUID
from pydantic import EmailStr, Field
from src.schemas.base import BaseSchema


class GenreSchema(BaseSchema):
    name: str


class GetGenreSchema(GenreSchema):
    id: UUID


class CreateGenreSchema(GenreSchema):
    pass


class UpdateGenrSchema(GenreSchema):
    pass