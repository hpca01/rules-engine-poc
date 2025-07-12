from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from .models import init_db, get_session, Event, EventAccepted
from .queue import Publisher, init_pub
from contextlib import asynccontextmanager
from functools import partial
from sqlmodel import Session, select
from sqlalchemy.engine import Engine
import json

engine: Engine = None
session = partial(get_session, engine)
queue = init_pub


@asynccontextmanager
async def init_resources(app: FastAPI):
    global session
    global engine
    engine = init_db()
    session = partial(get_session, engine)
    queue = init_pub()
    yield
    # close resources on program exit
    session.__exit__()
    await queue.close()
    engine.dispose(True)


app = FastAPI(lifespan=init_resources)


@app.post("/new_event")
async def new_event(
    request: Request,
    session: Session = Depends(session),
    queue: Publisher = Depends(queue),
) -> EventAccepted:
    # Insert payload into pgsql and queue for processing
    # return ID of insert
    json_payload = await request.json()
    obj = json.loads(json_payload)
    event = Event(event=json_payload)
    session.add(event)
    session.commit()
    assert event.id is not None, "Event ID is null, it is not commited"
    await queue.publish(
        obj["location"] if obj["location"] else "new",
        json_payload,
        obj["headers"] if obj["headers"] else None,
    )
    return EventAccepted(event_id=event.id)


@app.get("/health")
async def health(request: Request):
    return {"status": "Active"}


@app.get("/status/{event_id}", response_model=Event)
async def status(
    event_id: int, q: Union[str, None] = None, session: Session = Depends(session)
):
    # query pgsql by id using sqlmodel
    event = session.exec(select(Event, event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
