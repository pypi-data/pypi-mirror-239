import asyncio
from typing import Any

import aiohttp

from .backoff import Backoff
from .node import Node
from .player import Player

class Websocket:  # undocumented
    __slots__ = (
        "node",
        "socket",
        "retries",
        "retry",
        "_original_attempts",
        "backoff",
        "_listener_task",
        "_reconnect_task",
    )
    node: Node
    socket: aiohttp.ClientWebSocketResponse | None
    retries: int | None
    retry: float
    _original_attempts: int | None
    backoff: Backoff
    _listener_task: asyncio.Task[None] | None
    _reconnect_task: asyncio.Task[None] | None

    def __init__(self, *, node: Node) -> None: ...
    @property
    def headers(self) -> dict[str, str]: ...
    def is_connected(self) -> bool: ...
    async def connect(self) -> None: ...
    async def _reconnect(self) -> None: ...
    async def _listen(self) -> None: ...
    def get_player(self, payload: dict[str, Any]) -> Player | None: ...
    def dispatch(self, event: str, *args: Any, **kwargs: Any) -> None: ...
    async def cleanup(self) -> None: ...
