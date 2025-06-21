from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/new-event")
async def new_event(request:Request):
    json_payload = await request.json()
    return {"Hello": "World"}

@app.get("/health")
async def health(request:Request):
    return {"status": "Active"}

@app.get("/status/{item_id}")
async def status(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}