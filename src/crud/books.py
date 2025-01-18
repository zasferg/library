from sqlalchemy import select
from src.crud.base import BaseCrud, Schema
from src.models.initial_models import Book
from src.schemas.books import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class BookCrud(BaseCrud):
    base_model = Book
    get_schema = GetBookSchema
    update_schema = UpdateBookSchema
    create_schema = CreateBookSchema

    @classmethod
    async def get_all(cls, limit, offset, session: AsyncSession) -> List[Schema]:
        result = await session.execute(
            select(cls.base_model)
            .limit(limit)
            .offset(offset)
        )
        obj = result.unique().scalars().all()
        return [cls.get_schema.model_validate(item) for item in obj]

    @classmethod
    async def get_obj_by_param(
        cls, limit, offset, session: AsyncSession, **kwargs
    ) -> Schema | None:
        result = await session.execute(
            select(cls.base_model)
            .filter_by(**kwargs)
            .limit(limit)
            .offset(offset)
        )
        obj = result.scalars().first()
        return cls.get_schema.model_validate(obj)

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> Schema:
        instance = cls.base_model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
