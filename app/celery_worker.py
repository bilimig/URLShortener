import asyncio
from celery import Celery
from .config import settings
from . import crud, schemas
from .database import async_session_factory

celery = Celery(
    "tasks",
    broker=settings.BROKER_URL,
    backend=settings.BACKEND_URL
)

celery.conf.update(
    result_expires=3600,
)

@celery.task
def create_short_url_task(original_url: str) -> str:
    async def async_create_short_url():

        async with async_session_factory() as db:
          
            url_create = schemas.URLCreate(original_url=original_url)
            db_url = await crud.create_short_url(db=db, url=url_create)
            return db_url.short_url
           
    return asyncio.get_event_loop().run_until_complete(async_create_short_url())