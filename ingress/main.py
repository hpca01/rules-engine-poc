from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/new-event")
async def read_root(request:Request):
    json_payload = await request.json()
    return {"Hello": "World"}


@app.get("/status/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}