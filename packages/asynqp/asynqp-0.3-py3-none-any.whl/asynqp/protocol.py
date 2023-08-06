import asyncio
import struct
from . import spec
from . import frames
from .bases import Dispatcher
from .exceptions import AMQPError


class AMQP(asyncio.Protocol):
    def __init__(self, dispatcher, loop):
        self.dispatcher = dispatcher
        self.partial_frame = b''
        self.frame_reader = FrameReader()
        self.heartbeat_monitor = HeartbeatMonitor(self, loop, 0)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        while data:
            self.heartbeat_monitor.heartbeat_received()  # the spec says 'any octet may substitute for a heartbeat'

            try:
                result = self.frame_reader.read_frame(data)
            except AMQPError:
                self.transport.close()
                raise

            if result is None:  # incomplete frame, wait for the rest
                return
            frame, remainder = result

            self.dispatcher.dispatch(frame)
            if not remainder:
                return
            data = remainder

    def send_method(self, channel, method):
        frame = frames.MethodFrame(channel, method)
        self.send_frame(frame)

    def send_frame(self, frame):
        self.transport.write(frame.serialise())

    def send_protocol_header(self):
        self.transport.write(b'AMQP\x00\x00\x09\x01')

    def start_heartbeat(self, heartbeat_interval):
        self.heartbeat_monitor.start(heartbeat_interval)


class FrameReader(object):
    def __init__(self):
        self.partial_frame = b''

    def read_frame(self, data):
        data = self.partial_frame + data
        self.partial_frame = b''

        if len(data) < 7:
            self.partial_frame = data
            return

        frame_header = data[:7]
        frame_type, channel_id, size = struct.unpack('!BHL', frame_header)

        if len(data) < size + 8:
            self.partial_frame = data
            return

        raw_payload = data[7:7+size]
        frame_end = data[7+size]

        if frame_end != spec.FRAME_END:
            raise AMQPError("Frame end byte was incorrect")

        frame = frames.read(frame_type, channel_id, raw_payload)
        remainder = data[8+size:]

        return frame, remainder


class HeartbeatMonitor(object):
    def __init__(self, protocol, loop, heartbeat_interval):
        self.protocol = protocol
        self.loop = loop
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_timeout_callback = None

    def start(self, interval):
        if interval > 0:
            self.heartbeat_interval = interval
            self.send_heartbeat()
            self.monitor_heartbeat()

    def send_heartbeat(self):
        if self.heartbeat_interval > 0:
            self.protocol.send_frame(frames.HeartbeatFrame())
            self.loop.call_later(self.heartbeat_interval, self.send_heartbeat)

    def monitor_heartbeat(self):
        if self.heartbeat_interval > 0:
            self.heartbeat_timeout_callback = self.loop.call_later(self.heartbeat_interval * 2, self.heartbeat_timed_out)

    def heartbeat_received(self):
        if self.heartbeat_timeout_callback is not None:
            self.heartbeat_timeout_callback.cancel()
            self.monitor_heartbeat()

    def heartbeat_timed_out(self):
        self.protocol.send_method(0, spec.ConnectionClose(501, 'Heartbeat timed out', 0, 0))
