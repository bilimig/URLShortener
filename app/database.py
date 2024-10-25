from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()