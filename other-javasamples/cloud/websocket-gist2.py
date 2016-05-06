#!/usr/bin/python
#
# https://gist.githubusercontent.com/sadatanwer/222d4643c25f72293461/raw/1e94069a4c2711f63da41894df8be7e3b4a2768e/simple_websocket.py
# and adding 6 more lines here at the beginning of the file
#

import socket
import struct
import hashlib
import threading
import base64
import array
import time
from traceback import format_exc as format

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

cond = threading.Condition(threading.Lock())
msgQ = {}


def create_hash(key):
    reply = key + GUID
    sh1 = hashlib.sha1(reply)
    return sh1.digest()


def parse_headers(data):
    headers = {}
    lines = data.splitlines()
    for l in lines:
        parts = l.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    headers['code'] = lines[len(lines) - 1]
    return headers


def readData(client):
    try:
        data = client.recv(2)
        head1, head2 = struct.unpack('!BB', data)
        fin = bool(head1 & 0b10000000)
        opcode = head1 & 0b00001111
        if opcode == 1:
            length = head2 & 0b01111111
            if length == 126:
                data = client.recv(2)
                length, = struct.unpack('!H', data)
            elif length == 127:
                data = client.recv(8)
                length, = struct.unpack('!Q', data)

            mask_bits = client.recv(4)
            mask_bits = bytearray(mask_bits)
            data = client.recv(length)
            data = bytearray(data)
            DECODED = []
            for i in range(0, len(data)):
                DECODED.append(data[i] ^ mask_bits[i % 4])
            DECODED = array.array('B', DECODED).tostring()
            if fin:
                return DECODED
    except Exception, e:
        err = e.args[0]
        # this next if/else is a bit redundant, but illustrates how the
        # timeout exception is setup
        if err == 'timed out':
            pass
        elif err == 10053:
            return None
        else:
            print(e)
            return None


def handshake(client):
    client.setblocking(True)
    print('Starting hand shake')
    data = client.recv(1024)
    headers = parse_headers(data)
    digest = create_hash(
        headers['Sec-WebSocket-Key']
    )
    encoded_data = base64.b64encode(digest)
    shake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
    shake += "Upgrade: WebSocket\r\n"
    shake += "Connection: Upgrade\r\n"
    shake += "Sec-WebSocket-Origin: %s\r\n" % (headers['Origin'])
    shake += "Sec-WebSocket-Location: ws://%s/stuff\r\n" % (headers['Host'])
    shake += "Sec-WebSocket-Accept: %s\r\n\r\n" % encoded_data
    client.send(shake)
    print('Hand shake successful')


class WebSocketServer(object):
    def __init__(self, port):
        self.SERVER_END = False
        self.clients = {}
        self.port = port
        self._clientAvailable = threading.Lock()
        self._clientAvailable.acquire()
        self.SERVER_ACTIVE = True
        self.POLLER_ACTIVE = False
        self.numberClients = threading.Semaphore(0)
        self.lock = threading.Lock()

    def _bindClient(self):
        print('waiting connection')
        s = socket.socket()
        s.settimeout(5)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.port))
        s.listen(10)
        while self.SERVER_ACTIVE:
            try:
                conn, addr = s.accept()
                print('Client connected')
                self.lock.acquire()
                client = {'client': conn, 'failCount': 0, 'alive': True, 'messageQ': []}
                self.clients[conn.__hash__()] = client
                handshake(conn)
                # if not self.POLLER_ACTIVE:
                # threading.Thread(target=self._poll).start()
                self.numberClients.release()
                self.lock.release()
            except Exception, e:
                err = e.args[0]
                # this next if/else is a bit redundant, but illustrates how the
                # timeout exception is setup
                if err == 'timed out':
                    continue
                else:
                    print(format())
                    self.SERVER_ACTIVE = False
                    return
        print('Shutting down WS server port: %s' % self.port)
        return

    def _poll(self):
        self.POLLER_ACTIVE = True
        toRemove = []
        try:
            while self.SERVER_ACTIVE:
                print('Pinging...')
                self.sendData('ping')
                for clientCode in self.clients.keys():
                    client = self.clients[clientCode]['client']
                    client.settimeout(5)
                    try:
                        if self.clients[clientCode]['alive']:
                            reply = readData(client)
                            if reply is None:
                                print('no reply')
                                self.clients[clientCode]['failCount'] += 1
                                if self.clients[clientCode]['failCount'] > 2:
                                    self.clients[clientCode]['alive'] = False
                                    toRemove.append(clientCode)
                            elif reply == 'pong':
                                self.clients[clientCode]['alive'] = True
                        else:
                            print('%s Client lost' % clientCode)
                            toRemove.append(clientCode)
                    except Exception, e:
                        print('Thread for _poll crashed')
                        self.clients[clientCode]['alive'] = False
                        toRemove.append(clientCode)
                        print(e)
                for clientCode in toRemove:
                    self._remove(clientCode)
                toRemove = []
                if len(self.clients) == 0:
                    print('No Clients, shutting down poller')
                    self.POLLER_ACTIVE = False
                    return
                time.sleep(15)
        except Exception, e:
            self.POLLER_ACTIVE = False
            print(format())
            print(e)

    def startServer(self):
        threading.Thread(target=self._bindClient).start()

    def readData(self):
        reply = []
        for client in self.clients:
            reply.append(readData(client))

    def sendData(self, data, fin=True, opcode=1, masking_key=False):
        if fin > 0x1:
            raise ValueError('FIN bit parameter must be 0 or 1')
        if 0x3 <= opcode <= 0x7 or 0xB <= opcode:
            raise ValueError('Opcode cannot be a reserved opcode')

        ## +-+-+-+-+-------++-+-------------+-------------------------------+
        ## |F|R|R|R| opcode||M| Payload len |    Extended payload length    |
        ## |I|S|S|S|  (4)  ||A|     (7)     |             (16/63)           |
        ## |N|V|V|V|       ||S|             |   (if payload len==126/127)   |
        ## | |1|2|3|       ||K|             |                               |
        ## +-+-+-+-+-------++-+-------------+ - - - - - - - - - - - - - - - +
        ## +-+-+-+-+--------------------------------------------------------+
        ## |     Extended payload length continued, if payload len == 127   |
        ## + - - - - - - - - - - - - - - - +--------------------------------+
        ## + - - - - - - - - - - - - - - - +-------------------------------+
        ## |                               |Masking-key, if MASK set to 1  |
        ## +-------------------------------+-------------------------------+
        ## | Masking-key (continued)       |          Payload Data         |
        ## +-------------------------------- - - - - - - - - - - - - - - - +
        ## :                     Payload Data continued ...                :
        ## + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
        ## |                     Payload Data continued ...                |
        ## +---------------------------------------------------------------+
        try:
            header = struct.pack('!B', ((fin << 7)
                                        | (0 << 6)
                                        | (0 << 5)
                                        | (0 << 4)
                                        | opcode))
            if masking_key:
                mask_bit = 1 << 7
            else:
                mask_bit = 0

            length = len(data)
            if length < 126:
                header += struct.pack('!B', (mask_bit | length))
            elif length < (1 << 16):
                header += struct.pack('!B', (mask_bit | 126)) + struct.pack('!H', length)
            elif length < (1 << 63):
                header += struct.pack('!B', (mask_bit | 127)) + struct.pack('!Q', length)

            body = data
            for clientCode in self.clients.keys():
                client = self.clients[clientCode]['client']
                try:
                    client.send(bytes(header + body))
                except IOError, e:
                    print('error writing - %s' % data)
                    self._remove(clientCode)
        except Exception, e:
            print(format())
            print(e)

    def _remove(self, clientCode):
        acquire = False
        try:
            self.lock.acquire()
            acquire = True
            client = self.clients.pop(clientCode)
            client['client'].close()
            self.lock.release()
        except Exception, e:
            if acquire:
                self.lock.release()
            print(e)
            print(format())

    def close(self):
        self.SERVER_ACTIVE = False
        for clientCode in self.clients.keys():
            self.lock.acquire()
            client = self.clients.pop(clientCode)
            client['client'].close()
            self.lock.release()


# Initialize the socket connections at server end

# Test
if __name__ == '__main__':
    print('Started')
    ws = WebSocketServer(9999)
    ws.startServer()
    raw_input()
    ws.close()



