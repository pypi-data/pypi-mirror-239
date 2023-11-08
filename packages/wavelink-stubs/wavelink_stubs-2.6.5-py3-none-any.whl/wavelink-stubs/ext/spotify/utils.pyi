import enum
import re
from typing import Any, Final

__all__ = (
    "GRANTURL",
    "URLREGEX",
    "BASEURL",
    "RECURL",
    "SpotifyDecodePayload",
    "decode_url",
    "SpotifySearchType",
)

GRANTURL: Final[str]
URLREGEX: Final[re.Pattern[str]]
BASEURL: Final[str]
RECURL: Final[str]

class SpotifySearchType(enum.Enum):
    track: int
    album: int
    playlist: int
    unusable: int

class SpotifyDecodePayload:
    def __init__(self, *, type_: SpotifySearchType, id_: str) -> None: ...
    @property
    def type(self) -> SpotifySearchType: ...
    @property
    def id(self) -> str: ...
    def __getitem__(self, item: Any) -> SpotifySearchType | str: ...

def decode_url(url: str) -> SpotifyDecodePayload | None: ...
