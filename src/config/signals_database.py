from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.config import PG_HOST, PG_PASSWORD, PG_USERNAME

DATABASE_URL = f"postgresql+asyncpg://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}/SignlanDB"

SignalBASE = declarative_base()

signal_engine = create_async_engine(DATABASE_URL)

_async_session_maker = sessionmaker(
    bind=signal_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_signal_session() -> AsyncSession:
    async with _async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
