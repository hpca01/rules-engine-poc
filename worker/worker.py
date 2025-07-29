from abc import Protocol
from typing import Optional, Dict
import json
import os
import asyncio
import nats

class WorkerProto(Protocol):

    def __init__(self, *args, **kwargs):
        self.url = json.loads(os.environ.get("NATS_CLUSTER"))
        self.user = os.environ.get("NATS_USER")
        self.password = os.environ.get("NATS_PASS")
        self.port = os.environ.get("NATS_PORT")
        self._connect()
    
    def _connect(self):
        servers = [
            f"nats://{self.user}:{self.password}@{each_node}:{self.port}"
            for each_node in self.url
        ]
        self.nc = asyncio.run(nats.connect(servers=servers, max_reconnect_attempts=2))

    async def publish(self, topic: str, msg: str, headers: Optional[Dict[str, str]]):
        pass

    async def message_received(self, callback):
        pass

    async def message_response(self, callback):
        pass

