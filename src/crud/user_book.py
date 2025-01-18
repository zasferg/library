from src.crud.base import BaseCrud
from src.models.initial_models import BooksUsers
from src.schemas.user_book import *


class UserBookCrud(BaseCrud):
    base_model = BooksUsers
    get_schema = GetBookUserSchema
    create_schema = CreateBookUsersSchema
    update_schema = UpdateBookUsersSchema
