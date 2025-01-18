from src.crud.base import BaseCrud, Schema
from models.initial_models import Genre
from src.schemas.genres import *



class GenresCrud(BaseCrud):
    base_model = Genre
    get_schema = GetGenreSchema
    create_schema = CreateGenreSchema
    update_schema = UpdateGenrSchema
