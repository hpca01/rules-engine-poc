import asyncio
from typing import Any

import nats
from nats.errors import NoServersError


class Publisher:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.user = kwargs.get('user')
        self.password = kwargs.get('password')
        self.port = kwargs.get('port')
        if None in [self.url, self.user, self.password, self.port]:
            raise NoServersError('Your server setup is invalid need all of (url, user, pass, port)')
    
    async def connect(self):
        self.nc = await nats.connect(f"nats://{self.user}:{self.password}@{self.url}:{self.port}")
        return self

    def publish(self, topic:str, msg:Any):
        pass
