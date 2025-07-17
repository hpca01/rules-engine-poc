import asyncio
from typing import Any, Dict, Optional, List
import os
import json
from functools import partial

import nats
from nats.aio.client import Client
from nats.errors import NoServersError

class Publisher:
    def __init__(self, *args, **kwargs):
        self.url: List[str] = kwargs.get("url")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.port = kwargs.get("port")
        self.nc = None
        if None in [self.url, self.user, self.password, self.port]:
            raise NoServersError(
                "Your server setup is invalid need all of (url, user, pass, port)"
            )

    async def _new_error(self, exception:Exception):
        print(f'Got a conneciton error {exception}')

    async def connect(self):
        servers = [
            f"nats://{self.user}:{self.password}@{each_node}:{self.port}"
            for each_node in self.url
        ]
        cb = partial(Publisher._new_error, self)
        print(f"{servers=}")
        self.nc = await nats.connect(
            servers=servers, error_cb=cb, max_reconnect_attempts=2,
        )
        return self

    async def publish(self, topic: str, msg: str, headers: Optional[Dict[str, str]]):
        if self.nc is None or self.nc.is_closed:
            raise NoServersError("You have not connected to the server")
        else:
            if self.nc._status == Client.DISCONNECTED:
                raise NoServersError("No active server")
            return await self.nc.publish(
                topic,
                bytes(msg, encoding="utf8"),
                None,
                headers if headers else None,
            )

    async def close(self):
        await self.nc.close()


url = json.loads(os.environ.get("NATS_CLUSTER"))
user = os.environ.get("NATS_USER")
password = os.environ.get("NATS_PASS")
port = os.environ.get("NATS_PORT")
pub = Publisher(url=url, user=user, password=password, port=port)


async def get_pub() -> Publisher:
    if pub.nc is None:
        await pub.connect()
    return pub


async def close_pub():
    await pub.close()
