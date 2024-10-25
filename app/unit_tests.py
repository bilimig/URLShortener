import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from .database import Base
from .crud import create_short_url, get_url_by_short_url
from .schemas import URLCreate
from .models import URL
from .main import app, get_db


DATABASE_URL = "postgresql+asyncpg://test_user:test_password@db/test_db"
test_engine = create_async_engine(DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="function")
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    await test_engine.dispose()


@pytest.mark.asyncio
async def test_create_short_url(db_session):
    
    url_data = URLCreate(original_url="https://example.com")
    created_url = await create_short_url(db_session, url_data)

    assert created_url.original_url == "https://example.com"
    assert len(created_url.short_url) == 8

@pytest.mark.asyncio
async def test_get_url_by_short_url(db_session):
    
    url_data = URLCreate(original_url="https://example.com")
    created_url = await create_short_url(db_session, url_data)

    retrieved_url = await get_url_by_short_url(db_session, created_url.short_url)
    
    assert retrieved_url is not None
    assert retrieved_url.original_url == "https://example.com"

