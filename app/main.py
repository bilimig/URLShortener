from http.client import HTTPException
from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from . import models, schemas
from fastapi.staticfiles import StaticFiles
from .crud import get_url_by_short_url
from fastapi.templating import Jinja2Templates
import asyncio
from .database import async_session_factory, engine
from .celery_worker import create_short_url_task


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_tables()

async def get_db():
    async with async_session_factory() as session:
        yield session


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/shorten", response_model=schemas.URLResponse)
async def create_url(url: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    task = create_short_url_task.delay(url.original_url)

    timeout = 10
    while not task.ready():
        await asyncio.sleep(0.5)
        timeout -= 0.5
        if timeout <= 0:
            raise HTTPException(status_code=500, detail="Timeout while processing the URL.")

    if task.successful():
        db_url = task.result
    else:
        raise HTTPException(status_code=500, detail="Failed to create short URL. Probably it already exists.")

    return schemas.URLResponse(original_url=url.original_url, short_url=db_url)

@app.get("/{short_url}", response_model=schemas.URLResponse)
async def redirect_to_url(short_url: str, db: AsyncSession = Depends(get_db)):
    db_url = await get_url_by_short_url(db=db, short_url=short_url)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url