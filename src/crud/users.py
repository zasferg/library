from src.crud.base import BaseCrud
from src.models.initial_models import User
from src.schemas.users import *


class UserCrud(BaseCrud):
    base_model = User
    get_schema = GetUserSchema
    create_schema = CreateUserSchema
    update_schema = UpdateUserSchema
