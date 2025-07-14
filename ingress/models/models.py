from typing import Annotated, Optional, Dict
from datetime import datetime
from pydantic.dataclasses import dataclass
from pydantic import BaseModel

from sqlmodel import Field, Session, SQLModel, create_engine, select, TIMESTAMP
from sqlalchemy.engine import Engine
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import JSON
import os

class EventRequest(BaseModel):
    location:Optional[str]
    headers:Optional[Dict[str,str]]

class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at:Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True),
                                          sa_column_kwargs={'server_default': func.now()}, nullable=False)
    modified_at:Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True), sa_column_kwargs={'onupdate': func.now(), 'server_default':func.now()})
    event:Dict[str,str] = Field(sa_type=JSON, nullable=False)

@dataclass
class EventAccepted:
    event_id:int
