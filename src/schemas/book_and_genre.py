from datetime import date
from uuid import UUID
from src.schemas.base import BaseSchema


class BookGenreSchema(BaseSchema):
    books: UUID
    genres: UUID


class GetBookGenreSchema(BookGenreSchema):
    id: int


class CreateBookGenreSchema(BookGenreSchema):
    pass


class UpdateBookGenreSchema(BookGenreSchema):
    pass