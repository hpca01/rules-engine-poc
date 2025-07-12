from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from .models import Event, EventAccepted, EventRequest
from .db import init_db, get_session
from .queue import Publisher, init_pub
from contextlib import asynccontextmanager
from functools import partial
from sqlmodel import Session, select
from sqlalchemy.engine import Engine
import json

queue = init_pub


@asynccontextmanager
async def init_resources(app: FastAPI):
    init_db()
    queue = init_pub()
    yield
    # close resources on program exit
    await queue.close()


app = FastAPI(lifespan=init_resources)


@app.post("/new_event")
async def new_event(
    event:EventRequest,
    session: Session = Depends(get_session),
    queue: Publisher = Depends(queue),
) -> EventAccepted:
    # Insert payload into pgsql and queue for processing
    # return ID of insert
    print(f'{event=}')
    raw_obj = event.model_dump_json()
    obj=event
    event = Event(event=raw_obj)
    session.add(event)
    session.commit()
    print(f'db{event=}')
    assert event.id is not None, "Event ID is null, it is not commited"
    await queue.publish(
        obj.location if obj.location else "new",
        raw_obj,
        obj.headers if obj.headers else None,
    )
    return EventAccepted(event_id=event.id)


@app.get("/health")
async def health(request: Request):
    return {"status": "Active"}


@app.get("/status/{event_id}", response_model=Event)
async def status(
    event_id: int, q: Union[str, None] = None, session: Session = Depends(get_session)
):
    # query pgsql by id using sqlmodel
    event = session.exec(select(Event, event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
