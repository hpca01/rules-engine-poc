from typing import Union

from fastapi import FastAPI, Request, Depends
from models import init_db, get_session
from contextlib import asynccontextmanager
from functools import partial
from sqlmodel import Session

engine = None
session = partial(get_session, engine)

@asynccontextmanager
async def init_db_resources(app: FastAPI):
    global session
    global engine
    engine = init_db()
    session = partial(get_session, engine)
    yield

app = FastAPI(lifespan=init_db_resources)

@app.post("/new-event")
async def new_event(request:Request, session:Session = Depends(session)):
    #Insert payload into pgsql and queue for processing
    #return ID of insert
    json_payload = await request.json()
    return {"Hello": "World"}

@app.get("/health")
async def health(request:Request):
    return {"status": "Active"}

@app.get("/status/{item_id}")
async def status(item_id: int, q: Union[str, None] = None, session:Session = Depends(session)):
    #query pgsql by id using sqlmodel
    return {"item_id": item_id, "q": q}