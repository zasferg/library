from src.crud.base import BaseCrud
from models.initial_models import Token
from src.schemas.tokens import *


class TokenCrud(BaseCrud):
    base_model = Token
    get_schema = GetTokenSchema
    create_schema = CreateTokenSchema
    update_schema = UpdateTokenSchema
