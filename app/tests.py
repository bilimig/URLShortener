import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from .database import Base
from .main import app, get_db
from .models import URL


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
def override_get_db(db_session):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

@pytest.mark.asyncio
async def tests():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"original_url": "https://example.com"})

    assert response.status_code == 200
    assert "short_url" in response.json()
    assert response.json()["original_url"] == "https://example.com"


