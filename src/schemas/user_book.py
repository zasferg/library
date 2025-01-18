from datetime import date, datetime
from uuid import UUID
from src.schemas.base import BaseSchema


class BookUsersSchema(BaseSchema):
    books: UUID
    return_book_date: date


class CreateBookUsersSchema(BaseSchema):
    books: str
    return_book_date: date


class GetBookUserSchema(BookUsersSchema):
    id: int
    given_to_user_date: datetime


class UpdateBookUsersSchema(BookUsersSchema):
    pass
