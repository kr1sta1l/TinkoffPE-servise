from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


class GenericRepository:
    def __init__(self, db_engine, class_=AsyncSession):
        self._engine = db_engine
        self.async_session = sessionmaker(bind=db_engine, expire_on_commit=False, class_=class_)
        #
        # async def get_session() -> AsyncIterator[AsyncSession]:
        #     async with self.async_session() as session:
        #         yield session

        self._session: AsyncSession = self.async_session()

    async def save(self, entity):
        self._session.add(entity)
        await self._session.commit()

    async def delete(self, entity):
        await self._session.delete(entity)
        await self._session.commit()

    async def get(self, entity, id):
        # print(type(entity))
        # print(type(entity.id))
        return (await self._session.execute(select(entity).where(entity.id == id))).scalar_one_or_none()

    async def get_all(self, entity):
        entities = (await self._session.execute(select(entity))).scalars().all()
        return entities

    async def get_one_by_expression(self, entity, whereclause):
        return (await self._session.execute(select(entity).where(whereclause))).scalars().one_or_none()

    async def get_all_by_expression(self, entity, whereclause):
        return (await self._session.execute(select(entity).where(whereclause))).scalars().all()
