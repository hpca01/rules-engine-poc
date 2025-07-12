import asyncio
from typing import Any, Dict, Optional
import os

import nats
from nats.errors import NoServersError


class Publisher:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url")
        self.user = kwargs.get("user")
        self.password = kwargs.get("password")
        self.port = kwargs.get("port")
        if None in [self.url, self.user, self.password, self.port]:
            raise NoServersError(
                "Your server setup is invalid need all of (url, user, pass, port)"
            )

    async def connect(self):
        self.nc = await nats.connect(
            f"nats://{self.user}:{self.password}@{self.url}:{self.port}"
        )
        return self

    async def publish(self, topic: str, msg: str, headers: Optional[Dict[str, str]]):
        if not hasattr(self, "nc"):
            raise NoServersError("You have not connected to the server")
        else:
            return await self.nc.publish(
                topic, bytes(msg), None, headers if headers else None
            )

    async def close(self):
        await self.nc.close()


def init_pub() -> Publisher:
    url = os.environ.get("NATS_URL")
    user = os.environ.get("NATS_URL")
    password = os.environ.get("NATS_PASS")
    port = os.environ.get("NATS_PORT")
    return Publisher(url=url, user=user, password=password, port=port)
