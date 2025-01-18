from typing import List
from sqlalchemy import select
from src.crud.base import BaseCrud, Schema
from src.models.initial_models import Author
from src.schemas.authors import *
from sqlalchemy.ext.asyncio import AsyncSession


class AutorsCrud(BaseCrud):
    base_model = Author
    get_schema = GetAuthorSchema
    update_schema = UpdateAuthorSchema
    create_schema = CreateAuthorSchema

    @classmethod
    async def get_all(cls, limit, offset, session: AsyncSession) -> List[Schema]:
        result = await session.execute(
            select(cls.base_model).limit(limit).offset(offset)
        )
        obj = result.scalars().all()
        return [cls.get_schema.model_validate(item) for item in obj]

    @classmethod
    async def get_filtered_by_param(
        cls, limit, offset, session: AsyncSession, **kwargs
    ) -> Schema | None:

        result = await session.execute(
            select(cls.base_model).filter_by(**kwargs).limit(limit).offset(offset)
        )
        obj = result.scalars().all()
        return [cls.get_schema.model_validate(item) for item in obj]
