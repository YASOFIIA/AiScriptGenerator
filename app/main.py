from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.routers.bulk import router as bulk_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.uploads_path.mkdir(parents=True, exist_ok=True)
    settings.outputs_path.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(bulk_router)
