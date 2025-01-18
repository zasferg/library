import asyncio
from pydantic import EmailStr
from src.schemas.base import BaseSchema
from src.database import get_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.models.initial_models import User
from sqlalchemy import select
from src.auth.helpers.utils import hash_password
from src.database import engine

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class CreateSuperuserSchema(BaseSchema):
    email: EmailStr
    password: str


async def create_superuser(data: CreateSuperuserSchema, session: AsyncSession):

    try:
        result = await session.execute(select(User).filter(User.email == data.email))
        existing_user = result.scalars().one_or_none()

        if existing_user:
            raise ValueError("Данный пользователь уже в бд")

        new_superuser = User(
            email=data.email,
            password=hash_password(data.password),
            is_active=True,
            is_superuser=True,
        )

        session.add(new_superuser)
        await session.commit()
        await session.refresh(new_superuser)

        return new_superuser

    except Exception as e:
        raise e


async def main():
    async with async_session() as session:
        email = input("Введите email суперпользователя: ")
        password = input("Введите пароль суперпользователя: ")
        try:
            data = CreateSuperuserSchema(email=email, password=password)
            superuser = await create_superuser(data, session)
            return superuser
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise e


if __name__ == "__main__":
    asyncio.run(main())
