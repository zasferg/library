from sqlalchemy import select
from src.crud.base import BaseCrud,  Schema
from models.initial_models import User
from src.schemas.users import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.models.initial_models import Book


class UserCrud(BaseCrud):
    base_model = User
    get_schema = GetUserSchema
    create_schema = CreateUserSchema
    update_schema = UpdateUserSchema

