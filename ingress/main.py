from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from .models import Event, EventAccepted, EventRequest
from .db import init_db, get_session, close_db
from .db import init, get_db_session as get_session
from .queue import Publisher, get_pub, close_pub
from contextlib import asynccontextmanager
from functools import partial
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Engine
import traceback

healthy = False

@asynccontextmanager
async def init_resources(app: FastAPI):
    global healthy
    await init()
    healthy = True
    yield
    # close resources on program exit
    await close_pub()


app = FastAPI(lifespan=init_resources)

@app.post("/event")
async def new_event(
    event:EventRequest,
    session: AsyncSession = Depends(get_session),
    queue: Publisher = Depends(get_pub),
) -> EventAccepted:
    # Insert payload into pgsql and queue for processing
    # return ID of insert
    raw_obj = event.model_dump_json()
    obj=event
    event = Event(event=raw_obj)
    session.add(event)
    await session.flush()
    assert event.id is not None, "Event ID is null, it is not commited"
    try:
        await queue.publish(
            obj.location if obj.location else "new",
            raw_obj,
            obj.headers if obj.headers else None,
        )
    except Exception as e:
        global healthy
        healthy = False
        print(f'Error occurred {traceback.format_exc()}')
        await session.rollback()
        raise HTTPException(status_code=404, detail="Try request again")
    return EventAccepted(event_id=event.id)


@app.get("/health")
async def health(request: Request):
    global healthy
    if healthy:
        return {"status": "Active"}
    else:
        raise HTTPException(status_code=404, detail={'status': 'DED'})


@app.get("/status/{event_id}", response_model=Event)
async def status(
    event_id: int, q: Union[str, None] = None, session: Session = Depends(get_session)
):
    # query pgsql by id using sqlmodel
    event = session.exec(select(Event, event_id))
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
