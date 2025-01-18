import pytest
import asyncio
from src.models.initial_models import Base
from src.database import SessionLocal


async def clear_all_tables():
    async with SessionLocal() as session:
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
            await session.commit()


@pytest.fixture(scope="function", autouse=True)
def clear_tables():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(clear_all_tables())


def run_async(async_func, *args, **kwargs):
    session = SessionLocal()
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(async_func(session, *args, **kwargs))
    finally:
        loop.run_until_complete(session.close())
