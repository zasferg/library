from datetime import datetime
from typing import List, Optional
from uuid import UUID
from src.schemas.base import BaseSchema
from src.schemas.authors import GetAuthorSchema
from src.schemas.genres import GetGenreSchema


class BookSchema(BaseSchema):
    name: str | None
    description: str | None
    avaliable_copies: int | None


class GetBookSchema(BookSchema):
    id: UUID
    publication_date: datetime
    author: GetAuthorSchema
    genres: Optional[List[GetGenreSchema]] 

class CreateBookSchema(BookSchema):
    author: UUID
    genre: str


class UpdateBookSchema(BookSchema):
    pass
