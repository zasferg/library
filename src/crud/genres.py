from src.crud.base import BaseCrud, Schema
from models.initial_models import Genre
from src.schemas.genres import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class GenresCrud(BaseCrud):
    base_model = Genre
    get_schema = GetGenreSchema
    create_schema = CreateGenreSchema
    update_schema = UpdateGenrSchema
