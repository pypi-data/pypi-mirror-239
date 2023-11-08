from typing import TypeAlias, TypedDict

from .state import VoiceState

class Filters(TypedDict): ...

class _BaseRequest(TypedDict, total=False):
    voice: VoiceState
    position: int
    endTime: int
    volume: int
    paused: bool
    filters: Filters

class EncodedTrackRequest(_BaseRequest):
    encodedTrack: str | None

class IdentifierRequest(_BaseRequest):
    identifier: str

Request: TypeAlias = _BaseRequest | EncodedTrackRequest | IdentifierRequest
