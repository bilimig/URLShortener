from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
import hashlib
from sqlalchemy.future import select

async def create_short_url(db: AsyncSession, url: schemas.URLCreate):
    existing_url = await db.execute(select(models.URL).where(models.URL.original_url == url.original_url))
    existing_url = existing_url.scalars().first()

    if existing_url:
        return existing_url
    

    short_url = hashlib.md5(url.original_url.encode()).hexdigest()[:8]
    db_url = models.URL(original_url=url.original_url, short_url=short_url)
    
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)

    return db_url


async def get_url_by_short_url(db: AsyncSession, short_url: str):
    stmt = select(models.URL).where(models.URL.short_url == short_url)
    result = await db.execute(stmt)
    db_url = result.scalars().first()
    return db_url
