from typing import Annotated, Optional, Dict
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select, TIMESTAMP
from sqlalchemy.engine import Engine
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
import os

user=os.environ.get("POSTGRES_USER")
dbname=os.environ.get("POSTGRES_DB")
password = os.environ.get("POSTGRES_PASSWORD")
engine = create_engine(f"postgresql://{user}:{password}@db/{dbname}", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def close_db():
    engine.dispose(True)