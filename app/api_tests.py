import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from .database import Base
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

@pytest.fixture(autouse=True)
async def override_get_db(db_session):
    async def _override_get_db():
        async with db_session() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db

@pytest.mark.asyncio
async def test_create_url():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"original_url": "https://example.com"})
        
    assert response.status_code == 200
    assert "short_url" in response.json()
    assert response.json()["original_url"] == "https://example.com"

@pytest.mark.asyncio
async def test_redirect_to_url():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post("/shorten", json={"original_url": "https://example.com"})
        assert create_response.status_code == 200
        created_url = create_response.json()["short_url"]

        response = await ac.get(f"/{created_url}")
        assert response.status_code == 200
        assert response.json()["original_url"] == "https://example.com"
