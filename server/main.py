"""Description: Main entry point for the FastAPI application."""

from contextlib import asynccontextmanager

import uvicorn
from api import api_router
from config import ALLOWED_HOSTS, DEBUG, configure_logging
from database import engine
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Base

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown event
    await engine.dispose()


app = FastAPI(
    title="Server API",
    description="An API for FastAPI with PostgreSQL and Redis.",
    version="0.1.0",
    debug=DEBUG,
    host="0.0.0.0",
    port=8080,
    url_prefix="/api",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if DEBUG:
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    )

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
