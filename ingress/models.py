from typing import Annotated, Optional, Dict
from datetime import datetime
from pydantic.dataclasses import dataclass

from sqlmodel import Field, Session, SQLModel, create_engine, select, TIMESTAMP
from sqlalchemy.engine import Engine
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
import os


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at:Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True),
                                          sa_column_kwargs={'server_default': func.now()}, nullable=False)
    modified_at:Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True), sa_column_kwargs={'onupdate': func.now(), 'server_default':func.now()})
    event:Dict[str,str] = Field(sa_type=JSON, nullable=False)

@dataclass
class EventAccepted:
    event_id:int

engine = None 

def init_db():
    #TODO: Remove this as a global
    global engine
    user=os.environ.get("POSTGRES_USER")
    dbname=os.environ.get("POSTGRES_DB")
    password = os.environ.get("POSTGRES_PASSWORD")
    print(f'user {user} dbname {dbname} password {password} db')
    engine = create_engine(f"postgresql://{user}:{password}@db/{dbname}", echo=True)
    SQLModel.metadata.create_all(engine)
    return engine


def get_session(engine: Engine):
    with Session(engine) as session:
        yield session