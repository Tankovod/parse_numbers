from typing import List

from asyncpg import Type
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import INT, Column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import insert, select, create_engine
from src.settings import SETTINGS


class Base(DeclarativeBase):
    engine = create_async_engine(SETTINGS.DATABASE_ASYNC_URL)
    session = async_sessionmaker(bind=engine)

    id = Column(INT, primary_key=True)

    @classmethod
    async def insert_values(cls, instances: List[Type["Base"]]):
        async with cls.session() as session:
            session.add_all(instances)
            await session.commit()
            for instance in instances:
                await session.refresh(instance)
        return instances

    async def save(self):
        async with self.session() as session:  # type: AsyncSession
            session.add(self)
            await session.commit()
            await session.refresh(self)


