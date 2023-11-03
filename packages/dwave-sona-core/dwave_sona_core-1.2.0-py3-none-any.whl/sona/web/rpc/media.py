import asyncio
import json

from sona.core.stream.inferencer import StreamInferencerBase
from sona.core.stream.messages.context import EvtType, StreamContext
from sona.settings import settings

try:
    from aiortc import MediaStreamTrack, RTCPeerConnection
    from aiortc.mediastreams import MediaStreamError
except ImportError:
    pass

STREAM_INFERENCER_CLASS = settings.SONA_STREAM_INFERENCER_CLASS


class MediaInferencer:
    def __init__(self, inferencer_cls=STREAM_INFERENCER_CLASS) -> None:
        self.inferencer_cls = StreamInferencerBase.load_class(inferencer_cls)
        self.reply_queue = asyncio.Queue()
        self.inferencers = {}
        self.task = asyncio.create_task(self.reply())

    def addTrack(self, track: MediaStreamTrack, peer: RTCPeerConnection):
        inferencer: StreamInferencerBase = self.inferencer_cls()
        inferencer.setup()
        inferencer.on_load()
        inferencer.on_reply = lambda ctx: self.reply_queue.put_nowait((track, ctx))
        inferencer.reply_channel = peer.createDataChannel(f"reply_{track.id}")
        self.inferencers[track] = inferencer

    async def start(self):
        for track, inferencer in self.inferencers.items():
            inferencer.task = asyncio.create_task(self.run_track(track, inferencer))

    async def run_track(
        self, track: MediaStreamTrack, inferencer: StreamInferencerBase
    ):
        while True:
            try:
                frame = await track.recv()
                ctx = StreamContext(event_type=EvtType.AV_AUDIO, payload=frame)
                inferencer.on_context(ctx)
            except MediaStreamError:
                return

    async def stop(self, track):
        inferencer = self.inferencers[track]
        inferencer.on_stop()
        inferencer.task.cancel()

    async def stop_all(self, track=None):
        for inferencer in self.inferencers.values():
            inferencer.on_stop()
            inferencer.task.cancel()

    async def reply(self):
        while True:
            track, ctx = await self.reply_queue.get()
            inferencer = self.inferencers[track]
            inferencer.reply_channel.send(json.dumps(ctx.payload))
