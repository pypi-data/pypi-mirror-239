from typing import Any

from .enums import DiscordVoiceCloseType, TrackEventType
from .player import Player
from .tracks import Playable
from .types.events import EventOp

__all__ = (
    "TrackEventPayload",
    "WebsocketClosedPayload",
)

class TrackEventPayload:
    event: TrackEventType
    track: Playable
    original: Playable | None
    player: Player
    reason: str

    def __init__(self, *, data: EventOp, track: Playable, original: Playable | None, player: Player) -> None: ...

class WebsocketClosedPayload:
    code: DiscordVoiceCloseType
    reason: str
    by_discord: bool
    player: Player

    def __init__(self, *, data: dict[str, Any], player: Player) -> None: ...
