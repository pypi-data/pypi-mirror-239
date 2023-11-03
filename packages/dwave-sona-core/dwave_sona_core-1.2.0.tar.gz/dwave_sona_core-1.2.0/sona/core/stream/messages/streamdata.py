from typing import Any, Dict

import av
from pydantic import BaseModel

from .context import EvtType


class StreamData(BaseModel):
    _type: int
    data: Any

    @property
    def payload(self):
        return None


class DictStreamData(StreamData):
    _type: int = EvtType.DICT.value
    data: Dict

    @property
    def payload(self):
        return self.data


class RawStreamData(StreamData):
    _type: int = EvtType.RAW.value
    data: bytes

    @property
    def payload(self):
        return self.data


class AVAudioStreamData(StreamData):
    _type: int = EvtType.AV_AUDIO.value
    data: Any  # av.AudioFrame

    @property
    def raw(self):
        return bytes(self.data.planes[0])

    @property
    def sample_rate(self):
        return self.data.rate

    @property
    def bit_depth(self):
        return self.data.format.bits

    @property
    def channels(self):
        return len(self.data.layout.channels)

    @property
    def payload(self):
        return self.raw

    @classmethod
    def from_ndarray(cls, ndarray):
        cls(data=av.AudioFrame.from_ndarray(ndarray))

    @classmethod
    def to_ndarray(cls, ndarray):
        cls(data=av.AudioFrame.to_ndarray(ndarray))
