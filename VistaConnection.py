from RpcParameter import RpcParameter

__author__ = 'Joe'

import socket
from VistaException import VistaException
from VistaRpc import VistaRpc

class VistaConnection(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_connected = False

    def connect(self):
        my_hostname = socket.gethostname()
        my_ip = socket.gethostbyname(my_hostname)
        self.socket = None
        vista_info = socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        af, socktype, proto, canonname, sa = vista_info[0]
        try:
            self.socket = socket.socket(af, socktype, proto)
            self.socket.connect(sa)
        except socket.error as message:
            if self.socket:
                self.socket.close();
                self.socket = None
            raise VistaException('Unable to connect: ' + message)
        params = [
            RpcParameter(RpcParameter.LITERAL, my_ip),
            RpcParameter(RpcParameter.LITERAL, my_hostname)
        ]
        rpc = VistaRpc.prepare('HELLO', params)
        try:
            response = self.execute(rpc)
        except:
            raise VistaException('No VistA listener at ' + self.host + ', port ' + self.port)
        if response != 'accept':
            self.disconnect()
            raise VistaException('Connection not accepted: ' + response)
        self.is_connected = True

    def execute(self, rpc):
        self.send(rpc)
        return self.recv()

    def send(self, rpc):
        try:
            self.socket.send(rpc)
        except socket.error as message:
            raise VistaException('Error sending RPC: ' + message)

    def recv(self):
        # Header first...
        buf = self.socket.recv(256)
        if buf is None:
            raise VistaException('Error receiving: no response')

        # SECURITY error?
        if buf[0] != "\x00":
            buf = buf[1:ord(buf[0])]
            raise VistaException('VistA SECURITY error: ' + buf)

        # APPLICATION error?
        if buf[1] != "\x00":
            buf = buf[1:len(buf)]
            raise VistaException('VistA APPLICATION error: ' + buf)

        buf = buf[2:len(buf)]

        # Is there more response?
        end_idx = buf.find(VistaRpc.EOT)

        # If not, trim the EOT off the end
        if end_idx != -1: buf = buf[0:-1]

        # Sometimes there's a trailing '\0'
        if buf[-1] == "\x00": buf = buf[0:-1]

        # Here's the response so far...
        response = buf

        # Add to it if there's more...
        while end_idx == -1:
            buf = self.socket.recv(256)
            if buf is None:
                raise VistaException('Error receiving: no EOT and no MORE')

            # Is there more response?
            end_idx = buf.find(VistaRpc.EOT)

            # If not, trim the EOT off the end
            if end_idx != -1: buf = buf[0:-1]

            # Sometimes there's a trailing '\0'
            if buf[-1] == "\x00": buf = buf[0:-1]

            response += buf

        # Was there an error?
        if response.startswith('M  ERROR'):
            raise VistaException(response)

        return response

    def disconnect(self):
        if self.is_connected:
            rpc = VistaRpc.prepare('BYE')
            response = self.execute(rpc)
            self.socket.close()
            self.is_connected = False

