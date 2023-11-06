import asyncio
import collections
import contextlib
import logging

from . import codec, errors
from .transport import Transport

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BODYLESS_COMMANDS = (
    "handshake",
    "auth",
    "event",
    "force-leave",
    "tags",
    "stop",
    "respond",
)

STREAMING_COMMANDS = (
    "stream",
    "monitor",
    "query",
)


class Channel:
    TIMEOUT = 10

    def __init__(self):
        self._channel = collections.defaultdict(
            lambda: collections.defaultdict(asyncio.Queue)
        )

    async def send(self, key, value):
        chan = self._channel[key]
        if "Seq" in value:
            kind = "header"
        else:
            kind = "body"
        chan = chan[kind]
        await chan.put(value)

    async def recv(self, key, kind):
        chan = self._channel[key][kind]
        return (await chan.get(), chan)

    async def close(self, key):
        for chan in self._channel[key].values():
            async with asyncio.timeout(self.TIMEOUT):
                await chan.join()
        self._channel.pop(key, None)


class Protocol:
    CHANNEL = Channel
    TRANSPORT = Transport
    TIMEOUT = 10

    def __init__(self, transport):
        self.transport = transport
        self.channel = self.CHANNEL()

        self._buf = b""
        self._seq_send = 0
        self._seq_recv = 0

    @classmethod
    async def connect(cls, host="localhost", port=7373, auth_key=None):
        transport = await cls.TRANSPORT.connect(host, port)
        protocol = cls(transport)
        await protocol._handshake()
        if auth_key:
            await protocol._auth(auth_key)
        return protocol

    async def close(self):
        await self.transport.close()

    async def _recv(self):
        while True:
            err = False
            try:
                resp, self._buf = codec.decode(self._buf)
            except codec.DecodeError:
                err = True

            if err:
                self._buf += await self.transport.read()
                continue

            if "Seq" in resp:
                self._seq_recv = resp["Seq"]

            logger.debug("protocol._recv: %s %s", self._seq_recv, resp)
            await self.channel.send(self._seq_recv, resp)

    @contextlib.asynccontextmanager
    async def recv(self, req):
        async def gen(tasks):
            while True:
                tasks.append(asyncio.create_task(self._recv()))
                header, header_chan = await self.channel.recv(req["seq"], "header")
                header_chan.task_done()
                logger.debug("protocol.recv: %s", header)

                if req["command"] in BODYLESS_COMMANDS:
                    yield (header,)
                elif req["command"] in STREAMING_COMMANDS and not req.get("stream"):
                    req["stream"] = True
                    yield (header,)
                else:
                    tasks.append(asyncio.create_task(self._recv()))
                    body, body_chan = await self.channel.recv(req["seq"], "body")
                    body_chan.task_done()
                    logger.debug("protocol.recv: %s", body)
                    yield (header, body)

        try:
            tasks = []
            yield gen(tasks)
        finally:
            for task in tasks:
                task.cancel()
            finished_tasks, pending_tasks = await asyncio.wait(tasks)
            for task in finished_tasks:
                try:
                    task.result()
                except asyncio.CancelledError:
                    pass
            await self.channel.close(req["seq"])

    async def send(self, req):
        req["seq"], self._seq_send = self._seq_send, self._seq_send + 1
        data = codec.encode(
            seq=req["seq"], command=req["command"], body=req.get("body")
        )
        await self.transport.write(data)
        return req

    async def _handshake(self):
        req = await self.send(
            {
                "command": "handshake",
                "body": {"Version": 1},
            }
        )

        async with self.recv(req) as resp:
            async with asyncio.timeout(self.TIMEOUT):
                resp = await anext(resp)

        if req["seq"] != resp[0]["Seq"]:
            raise errors.SerfError("connection.handshake: invalid sequence number")
        if resp[0]["Error"]:
            raise errors.SerfError("connection.handshake: {}".format(resp["Error"]))

    async def _auth(self, auth_key):
        req = await self.send(
            {
                "command": "auth",
                "body": {"AuthKey": auth_key},
            }
        )

        async with self.recv(req) as stream:
            async with asyncio.timeout(self.TIMEOUT):
                resp = await anext(stream)

        if req["seq"] != resp[0]["Seq"]:
            raise errors.SerfError("connection.auth: invalid sequence number")
        if resp[0]["Error"]:
            raise errors.SerfError("connection.auth: {}".format(resp["Error"]))
