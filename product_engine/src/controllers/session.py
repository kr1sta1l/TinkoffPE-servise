from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from database.db import db_settings
from repository.generic_repository import GenericRepository

engine = create_async_engine(db_settings["database_url"], echo=db_settings["echo"])
# async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# async def get_session() -> AsyncIterator[AsyncSession]:
#     async with async_session() as session:
#         yield session


repository = GenericRepository(engine)
