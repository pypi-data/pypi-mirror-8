# coding=utf-8
from __future__ import absolute_import
from .event_emitter import EventEmitter
from . import has_bin
from . import parser
import logging

logger = logging.getLogger(__name__)

__all__ = ['Socket', 'flags']

# these events are preserved for internal usage, socket can't emit these to clients
events = [
    'error',
    'connect',
    'disconnect',
]

flags = [
    'json',
    'volatile',  # volatile flag indicates that the upcoming packets are not important, can be lost in some cases
    'broadcast',  # broadcast flag indicates that the upcoming packet should be broadcast to all sockets in the namespace
]


class Socket(EventEmitter):
    """
    [connection, namespace] defines a socket
    """

    def __init__(self, namespace, client):
        super(Socket, self).__init__()

        self.namespace = namespace
        self.adapter = namespace.adapter
        self.server = namespace.server
        self.id = client.id
        self.client = client
        self.engine_socket = client.engine_socket
        self.rooms = []
        self.rooms_send_to = []
        self.flags = set()
        self.acks = {}
        self.connected = True

    def emit(self, event, *args, **kwargs):
        """
        the interface for both sending messages and normal event notification
        If the event is predefined events, then emit the event to listeners, otherwise
        send it out as packet
        :param event: Event name
        :param args: The list of data for the event. emit('message', 'hello') or emit('message', {'content':'wonderful'})
        :return: None
        """
        if event in events:
            super(Socket, self).emit(event, *args)

        else:
            packet = {'type': parser.EVENT}

            if has_bin(args):
                packet['type'] = parser.BINARY_EVENT

            packet['data'] = [event] + list(args)

            broadcast = len(self.rooms_send_to) > 0 or 'broadcast' in self.flags

            if 'callback' in kwargs:
                if broadcast:
                    raise RuntimeError('Callback not supported in broadcast packet')

                self.debug('emitting packet with ack id %d' % self.namespace.ids)

                packet['id'] = self.namespace.ids
                self.namespace.ids += 1
                self.acks[packet['id']] = kwargs['callback']

            if broadcast:
                self.adapter.broadcast(packet, {
                    'except': [self.id],
                    'rooms': self.rooms_send_to,
                    'flags': self.flags
                })
            else:
                self.packet(packet)

        self.rooms_send_to = []
        self.flags = set()

    def to(self, name):
        """
        Mark that the next event should send to which room
        :param name: The name of the room
        :return: self. Easier for chaining. socket.to('chat').emit('message', 'hello chat')
        """
        if name not in self.rooms_send_to:
            self.rooms_send_to.append(name)

        return self

    def send(self, *args):

        self.emit('message', *args)
        return self

    write = send

    def packet(self, p, pre_encoded=False):
        if type(p) is dict:
            p['nsp'] = self.namespace.name
        self.client.packet(p, pre_encoded)

    def join(self, room, callback=None):
        self.debug('joining room %s' % room)
        if room in self.rooms:
            return self

        def cb(err=None):
            if err:
                return cb and cb(err)
            self.debug('joined room %s' % room)
            self.rooms.append(room)
            callback and callback()

        self.adapter.add(self.id, room)
        return self

    def leave(self, room, callback=None):
        self.debug('leaving room %s' % room)

        def cb(err):
            if err:
                return callback and callback(err)

            self.debug('left room %s' % room)
            self.rooms.remove(room)
            callback and callback()

        self.adapter.remove(self.id, room, cb)
        return self

    def leave_all(self):
        self.adapter.remove_all(self.id)
        self.rooms = []

    def on_connect(self, *args, **kwargs):
        self.debug('socket connected - writing packet')
        self.join(self.id)
        self.packet({'type': parser.CONNECT})
        self.namespace.connected[self.id] = self

    def on_packet(self, packet, *args, **kwargs):
        self.debug('got packet %s' % packet['type'])

        _type = packet['type']

        if _type == parser.EVENT:
            self.on_event(packet)
        elif _type == parser.BINARY_EVENT:
            self.on_event(packet)
        elif _type == parser.ACK:
            self.on_ack(packet)
        elif _type == parser.BINARY_ACK:
            self.on_ack(packet)
        elif _type == parser.DISCONNECT:
            self.on_disconnect()
        elif _type == parser.ERROR:
            self.emit('error', packet["data"])

    def on_event(self, packet):

        packet_data = packet.get('data', [])

        event = packet_data.pop(0)
        if len(packet_data) == 1:
            packet_data = packet_data[0]

        super(Socket, self).emit(event, packet_data)

        if 'id' in packet:
            _type = parser.ACK if not has_bin(packet['data']) else parser.BINARY_ACK
            self.packet({
                'id': packet['id'],
                'type': _type,
                'data': [event, packet_data]
            })

    def on_ack(self, packet):
        if 'id' not in packet or packet['id'] not in self.acks:
            self.debug('bad ack %s %s' % (packet, self.acks))
        else:
            _id = packet['id']
            ack = self.acks[_id]
            self.debug('calling ack %s with %s' % (_id, unicode(packet['data'])))
            event = packet['data'][0]
            if len(packet['data']) > 1:
                data = packet['data'][1]
            else:
                data = None
            ack(event, data)
            self.acks.pop(_id)

    def on_disconnect(self):
        self.debug('got disconnect packet')
        self.on_close('client namespace disconnect')

    def on_close(self, reason=None, *args, **kwargs):
        self.debug("On close %s" % reason)

        if not self.connected:
            return

        self.debug('closing socket - reason %s' % reason)
        self.leave_all()
        self.namespace.remove(self)
        self.namespace.connected.pop(self.id)
        self.client.remove(self)
        self.connected = False
        self.emit('disconnect', reason)
        self.debug('socket closed')

    def disconnect(self, close):
        if not self.connected:
            return self

        if close:
            self.client.disconnect()
        else:
            self.packet({
                'type': parser.DISCONNECT
            })
            self.on_close('server namespace disconnect')

        return self

    @property
    def context(self):
        return self.engine_socket.context

    def flag(self, flag):
        self.flags.add(flag)
        return self

    def debug(self, message):
        logger.debug("[SocketIOSocket(%s)][%s][C:%d] %s" % (self.namespace.name, self.id,  int(self.connected), message))
