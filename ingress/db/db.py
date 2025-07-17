from typing import Annotated, Optional, Dict
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select, TIMESTAMP
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
import os

user=os.environ.get("POSTGRES_USER")
dbname=os.environ.get("POSTGRES_DB")
password = os.environ.get("POSTGRES_PASSWORD")
# engine = create_engine(f"postgresql://{user}:{password}@db/{dbname}", echo=True)
engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@db/{dbname}", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print(f'Created tables')


def get_session():
    with Session(engine) as session:
        yield session

async def get_db_session():
    session = AsyncSessionLocal()
    yield session

def close_db():
    engine.dispose(True)

async def db_close():
    await engine.dispose(True)