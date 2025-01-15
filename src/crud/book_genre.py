from src.crud.base import BaseCrud
from src.models.initial_models import BooksGenres
from src.schemas.book_and_genre import *

class BookGenreCrud(BaseCrud):
    base_model = BooksGenres
    get_schema = GetBookGenreSchema
    update_schema = UpdateBookGenreSchema
    create_schema = CreateBookGenreSchema


    