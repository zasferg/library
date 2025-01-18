import pytest
import asyncio
from src.models.initial_models import Base
from src.models.initial_models import User
from src.auth.helpers.utils import hash_password
from src.database import SessionLocal


async def clear_all_tables():
    async with SessionLocal() as session:
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()


async def create_superuser():
    async with SessionLocal() as session:
        new_superuser = User(
            email="admin@admin.com",
            password=hash_password("1111"),
            is_active=True,
            is_superuser=True,
        )
        session.add(new_superuser)
        await session.commit()
        await session.refresh(new_superuser)

        return new_superuser


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_all_tables())


@pytest.fixture(scope="function", autouse=True)
def create_superuser_loop():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_superuser())


def run_async(async_func, *args, **kwargs):
    session = SessionLocal()
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(async_func(session, *args, **kwargs))
    finally:
        loop.run_until_complete(session.close())
