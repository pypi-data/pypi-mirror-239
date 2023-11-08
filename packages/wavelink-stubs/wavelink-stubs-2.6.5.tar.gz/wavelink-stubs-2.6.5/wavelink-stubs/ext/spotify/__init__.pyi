import asyncio
from collections.abc import AsyncIterator
from typing import Any, TypeVar
from typing_extensions import Self

import aiohttp

from discord.ext import commands
from wavelink import Node, Playable, Player

from .utils import SpotifyDecodePayload, SpotifySearchType, decode_url

__all__ = (
    "SpotifySearchType",
    "SpotifyClient",
    "SpotifyTrack",
    "SpotifyRequestError",
    "decode_url",
    "SpotifyDecodePayload",
)

_BotT_co = TypeVar("_BotT_co", bound=commands.Bot | commands.AutoShardedBot, covariant=True)
_PlayableT = TypeVar("_PlayableT", bound=Playable)

class SpotifyAsyncIterator(AsyncIterator[SpotifyTrack]):  # undocumented
    _query: str
    _limit: int
    _type: SpotifySearchType
    _node: Node
    _first: bool
    _count: int
    _queue: asyncio.Queue[SpotifyTrack]

    def __init__(self, *, query: str, limit: int, type: SpotifySearchType, node: Node) -> None: ...
    def __aiter__(self) -> Self: ...
    async def fill_queue(self) -> None: ...
    async def __anext__(self) -> SpotifyTrack: ...

class SpotifyRequestError(Exception):
    status: int
    reason: str | None

    def __init__(self, status: int, reason: str | None = ...) -> None: ...

class SpotifyTrack:
    __slots__ = (
        "raw",
        "album",
        "images",
        "artists",
        "name",
        "title",
        "uri",
        "id",
        "length",
        "duration",
        "explicit",
        "isrc",
        "__dict__",
    )
    raw: dict[str, Any]
    album: str
    images: list[str]
    artists: list[str]
    genres: list[str]
    name: str
    title: str
    uri: str
    id: str
    isrc: str | None
    length: int
    duration: int
    explicit: bool

    def __init__(self, data: dict[str, Any]) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    @classmethod
    async def search(
        cls,
        query: str,
        *,
        node: Node | None = ...,
    ) -> list[Self]: ...
    @classmethod
    def iterator(
        cls,
        *,
        query: str,
        limit: int | None = ...,
        node: Node | None = ...,
    ) -> SpotifyAsyncIterator: ...
    @classmethod
    async def convert(cls, ctx: commands.Context[_BotT_co], argument: str) -> Self: ...
    async def fulfill(self, *, player: Player, cls: type[_PlayableT], populate: bool) -> _PlayableT: ...

class SpotifyClient:
    session: aiohttp.ClientSession

    def __init__(self, *, client_id: str, client_secret: str) -> None: ...
    @property
    def grant_headers(self) -> dict[str, Any]: ...
    @property
    def bearer_headers(self) -> dict[str, Any]: ...
    def is_token_expired(self) -> bool: ...
