import enum

__all__ = (
    "NodeStatus",
    "TrackSource",
    "LoadType",
    "TrackEventType",
    "DiscordVoiceCloseType",
)

class NodeStatus(enum.Enum):
    DISCONNECTED: int
    CONNECTING: int
    CONNECTED: int

class TrackSource(enum.Enum):
    YouTube: int
    YouTubeMusic: int
    SoundCloud: int
    Local: int
    Unknown: int

class LoadType(enum.Enum):
    track_loaded: str
    playlist_loaded: str
    search_result: str
    no_matches: str
    load_failed: str

class TrackEventType(enum.Enum):
    START: str
    END: str

class DiscordVoiceCloseType(enum.Enum):
    CLOSE_NORMAL: int
    UNKNOWN_OPCODE: int
    FAILED_DECODE_PAYLOAD: int
    NOT_AUTHENTICATED: int
    AUTHENTICATION_FAILED: int
    ALREADY_AUTHENTICATED: int
    SESSION_INVALID: int
    SESSION_TIMEOUT: int
    SERVER_NOT_FOUND: int
    UNKNOWN_PROTOCOL: int
    DISCONNECTED: int
    VOICE_SERVER_CRASHED: int
    UNKNOWN_ENCRYPTION_MODE: int
