from src.crud.base import BaseCrud
from src.models.initial_models import Author
from src.schemas.authors import *

class AutorsCrud(BaseCrud):
    base_model = Author
    get_schema = GetAuthorSchema
    update_schema = UpdateAuthorSchema
    create_schema = CreateAuthorSchema