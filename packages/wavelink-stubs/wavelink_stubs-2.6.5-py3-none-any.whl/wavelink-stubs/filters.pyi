import abc
from typing import Any
from typing_extensions import Self

__all__ = (
    "BaseFilter",
    "Equalizer",
    "Karaoke",
    "Timescale",
    "Tremolo",
    "Vibrato",
    "Rotation",
    "Distortion",
    "ChannelMix",
    "LowPass",
    "Filter",
)

class BaseFilter(abc.ABC):
    name: str
    def __init__(self, name: str | None = None) -> None: ...

class Equalizer(BaseFilter):
    bands: list[dict[str, float]]
    def __init__(self, name: str = ..., *, bands: list[tuple[int, float]]) -> None: ...
    @property
    @classmethod
    def flat(cls) -> Self: ...
    @classmethod
    def boost(cls) -> Self: ...
    @classmethod
    def metal(cls) -> Self: ...
    @classmethod
    def piano(cls) -> Self: ...

class Karaoke(BaseFilter):
    level: float
    mono_level: float
    filter_band: float
    filter_width: float

    def __init__(
        self,
        *,
        level: float = ...,
        mono_level: float = ...,
        filter_band: float = ...,
        filter_width: float = ...,
    ) -> None: ...

class Timescale(BaseFilter):
    speed: float
    pitch: float
    rate: float

    def __init__(self, *, speed: float = ..., pitch: float = ..., rate: float = ...) -> None: ...

class Tremolo(BaseFilter):
    frequency: float
    depth: float
    def __init__(self, *, frequency: float = ..., depth: float = ...) -> None: ...

class Vibrato(BaseFilter):
    frequency: float
    depth: float

    def __init__(self, *, frequency: float = ..., depth: float = ...) -> None: ...

class Rotation(BaseFilter):
    speed: float

    def __init__(self, speed: float = ...) -> None: ...

class Distortion(BaseFilter):
    sin_offset: float
    sin_scale: float
    cos_offset: float
    cos_scale: float
    tan_offset: float
    tan_scale: float
    offset: float
    scale: float

    def __init__(
        self,
        *,
        sin_offset: float = ...,
        sin_scale: float = ...,
        cos_offset: float = ...,
        cos_scale: float = ...,
        tan_offset: float = ...,
        tan_scale: float = ...,
        offset: float = ...,
        scale: float = ...,
    ) -> None: ...

class ChannelMix(BaseFilter):
    left_to_left: float
    right_to_right: float
    left_to_right: float
    right_to_left: float

    def __init__(
        self,
        *,
        left_to_left: float = ...,
        left_to_right: float = ...,
        right_to_left: float = ...,
        right_to_right: float = ...,
    ) -> None: ...
    @classmethod
    def mono(cls) -> Self: ...
    @classmethod
    def only_left(cls) -> Self: ...
    @classmethod
    def full_left(cls) -> Self: ...
    @classmethod
    def only_right(cls) -> Self: ...
    @classmethod
    def full_right(cls) -> Self: ...
    @classmethod
    def switch(cls) -> Self: ...

class LowPass(BaseFilter):
    smoothing: float

    def __init__(self, *, smoothing: float = ...) -> None: ...

class Filter:
    filter: Filter | None
    equalizer: Equalizer | None
    karaoke: Karaoke | None
    timescale: Timescale | None
    tremolo: Tremolo | None
    vibrato: Vibrato | None
    rotation: Rotation | None
    distortion: Distortion | None
    channel_mix: ChannelMix | None
    low_pass: LowPass | None

    def __init__(
        self,
        _filter: Filter | None = ...,
        *,
        equalizer: Equalizer | None = ...,
        karaoke: Karaoke | None = ...,
        timescale: Timescale | None = ...,
        tremolo: Tremolo | None = ...,
        vibrato: Vibrato | None = ...,
        rotation: Rotation | None = ...,
        distortion: Distortion | None = ...,
        channel_mix: ChannelMix | None = ...,
        low_pass: LowPass | None = ...,
    ) -> None: ...
    @property
    def _payload(self) -> dict[str, Any]: ...  # undocumented
