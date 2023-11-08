from typing import TypeVar

import aiohttp

import discord
from discord.utils import classproperty

from .enums import NodeStatus
from .ext import spotify
from .player import Player
from .tracks import Playable, Playlist

_PlayableT = TypeVar("_PlayableT", bound=Playable)
_PlaylistT = TypeVar("_PlaylistT", bound=Playlist)

__all__ = (
    "Node",
    "NodePool",
)

class Node:
    heartbeat: float
    client: discord.Client | None

    def __init__(
        self,
        *,
        id: str | None = ...,
        uri: str,
        password: str,
        secure: bool = ...,
        use_http: bool = ...,
        session: aiohttp.ClientSession = ...,
        heartbeat: float = ...,
        retries: int | None = ...,
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def id(self) -> str: ...
    @property
    def uri(self) -> str: ...
    @property
    def password(self) -> str: ...
    @property
    def players(self) -> dict[int, Player]: ...
    @property
    def status(self) -> NodeStatus: ...
    def get_player(self, guild_id: int, /) -> Player | None: ...
    async def get_tracks(self, cls: type[_PlayableT], query: str) -> list[_PlayableT]: ...
    async def get_playlist(self, cls: type[_PlaylistT], query: str) -> _PlaylistT | None: ...
    async def build_track(self, *, cls: type[_PlayableT], encoded: str) -> _PlayableT: ...

class NodePool:
    @classmethod
    async def connect(
        cls,
        *,
        client: discord.Client,
        nodes: list[Node],
        spotify: spotify.SpotifyClient | None = ...,
    ) -> dict[str, Node]: ...
    @classproperty
    def nodes(cls) -> dict[str, Node]: ...
    @classmethod
    def get_node(cls, id: str | None = ...) -> Node: ...
    @classmethod
    def get_connected_node(cls) -> Node: ...
    @classmethod
    async def get_tracks(
        cls_,  # type: ignore [reportSelfClsParameterName]
        query: str,
        *,
        cls: type[_PlayableT],
        node: Node | None = ...,
    ) -> list[_PlayableT]: ...
    @classmethod
    async def get_playlist(
        cls_,  # type: ignore [reportSelfClsParameterName]
        query: str,
        *,
        cls: type[_PlaylistT],
        node: Node | None = ...,
    ) -> _PlaylistT | None: ...
