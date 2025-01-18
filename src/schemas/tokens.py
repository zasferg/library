from datetime import datetime
from uuid import UUID
from src.schemas.base import BaseSchema


class TokenSchema(BaseSchema):
    refresh_token: str
    user_id: UUID
    created_at: datetime


class GetTokenSchema(TokenSchema):
    id: UUID


class CreateTokenSchema(TokenSchema):
    pass


class UpdateTokenSchema(TokenSchema):
    pass
