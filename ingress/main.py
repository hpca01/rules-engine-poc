from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from .models import init_db, get_session, Event, EventAccepted
from contextlib import asynccontextmanager
from functools import partial
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

engine:Engine = None
session = partial(get_session, engine)

@asynccontextmanager
async def init_db_resources(app: FastAPI):
    global session
    global engine
    engine = init_db()
    session = partial(get_session, engine)
    yield
    #close on program exit
    session.__exit__()
    engine.dispose(True)

app = FastAPI(lifespan=init_db_resources)

@app.post("/new_event")
async def new_event(request:Request, session:Session = Depends(session))->EventAccepted:
    #Insert payload into pgsql and queue for processing
    #return ID of insert
    json_payload = await request.json()
    event = Event(event=json_payload)
    session.add(event)
    session.commit()
    assert event.id is not None, "Event ID is null, it is not commited"
    return EventAccepted(event_id=event.id)

@app.get("/health")
async def health(request:Request):
    return {"status": "Active"}

@app.get("/status/{event_id}", response_model=Event)
async def status(event_id: int, q: Union[str, None] = None, session:Session = Depends(session)):
    #query pgsql by id using sqlmodel
    event = session.exec(select(Event, event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event