from enum import IntEnum
from typing import Any, Dict

from sona.core.messages import MessageBase


class EvtType(IntEnum):
    DICT = 0
    RAW = 1
    RAW_AUDIO = 2
    RAW_VIDEO = 3
    AV_AUDIO = 4


class StreamContext(MessageBase):
    event_type: int
    header: Dict = {}
    payload: Any = None

    def to_packet(self):
        return (self.event_type, self.header, self.payload)

    @classmethod
    def from_packet(cls, msg):
        return cls(event_type=msg[0], header=msg[1], payload=msg[2])
