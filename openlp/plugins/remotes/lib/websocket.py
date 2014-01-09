# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

"""
Simple implementation of RFC 6455 for websocket protocol in a very simple and focused manner, just for the purposes
of this application
"""

import logging
import re
import socketserver
import threading
import time
import socket
import base64
import uuid

from base64 import b64encode
from hashlib import sha1

HOST, PORT = '', 8888
WEB_SOCKETS_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'.encode('utf-8')
WEB_SOCKETS_RESPONSE_TEMPLATE = (
    'HTTP/1.1 101 Switching Protocols',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}',
    'Upgrade: websocket',
    '',
    '',
)
WEB_SOCKETS_HANDSHAKE_ERROR = 'Error: Handshake'.encode('utf-8')
WEB_SOCKET_CLIENT_HEADERS = (
        "GET / HTTP/1.1",
        "Upgrade: websocket",
        "Connection: Upgrade",
        "Host: {host}:{port}",
        "Origin: null",
        "Sec-WebSocket-Key: {key}",
        "Sec-WebSocket-Version: 13",
        "",
        "",
)


class ThreadedWebSocketHandler(socketserver.BaseRequestHandler):
    """
    ThreadedWebSocketHandler implements the upgrade handshake and continues to serve the socket
    """
    def handle(self):
        """
        Called once per connection, the connection will not be added to the list of clients
        until the handshake has succeeded
        """
        has_upgraded = False
        data_buffer = ''
        while True:
            data_string = ''
            data_received = ''
            try:
                data_received = self.request.recv(1024)
            except Exception as e:
                #print(self.client_address, e.errno, e.strerror)
                if e.errno == 10053 or e.errno == 10054:
                    self.server.remove_client(self)
                    break
            if len(data_received) > 0:
                #print(" data_received: ", data_received)
                if has_upgraded:
                    data_string = ThreadedWebSocketHandler.decode_websocket_message(data_received)
                else:
                    data_string = data_received.decode('utf-8', 'ignore')
            if len(data_string) > 0:
                #print(" from: ", self.client_address, " data: ", data_string, " upgraded: ", has_upgraded)
                if not has_upgraded:
                    data_buffer += data_string
                    #print("x", data_buffer, "x")
                    if data_buffer[0] != 'G':
                        #print("return error")
                        self.request.send(WEB_SOCKETS_HANDSHAKE_ERROR)
                        break
                    match = re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', data_buffer)
                    #print("match: ", match)
                    if match:
                        received_key = (match.groups()[0].strip()).encode('utf-8')
                        generated_key = sha1(received_key + WEB_SOCKETS_GUID).digest()
                        response_key = b64encode(generated_key).decode('utf-8')
                        response = ('\r\n'.join(WEB_SOCKETS_RESPONSE_TEMPLATE).format(key=response_key)).encode('utf-8')
                        #print(response)
                        self.request.send(response)
                        has_upgraded = True
                        data_buffer = ''
                        self.server.add_client(self)

    @staticmethod
    def decode_websocket_message(byte_array):
        """
        decode_websocket_message decodes the messages sent from a websocket client according to RFC 6455
        :param byte_array: an array of bytes as received from the socket
        :return: returns a string
        """
        data_length = byte_array[1] & 127
        index_first_mask = 2
        if data_length == 126:
            index_first_mask = 4
        elif data_length == 127:
            index_first_mask = 10
        masks = [m for m in byte_array[index_first_mask: index_first_mask + 4]]
        index_first_data_byte = index_first_mask + 4
        decoded_chars = []
        index = index_first_data_byte
        secondary_index = 0
        while index < len(byte_array):
            char = chr(byte_array[index] ^ masks[secondary_index % 4])
            #print(char)
            decoded_chars.append(char)
            index += 1
            secondary_index += 1
        return ''.join(decoded_chars)

    @staticmethod
    def encode_websocket_message(message):
        """
        encode_websocket_message encodes a message prior to sending to a websocket client according to RFC 6455
        :param message: string to be encoded
        :return: the message encoded into a byte array
        """
        frame_head = bytearray(2)
        frame_head[0] = ThreadedWebSocketHandler.set_bit(frame_head[0], 7)
        frame_head[0] = ThreadedWebSocketHandler.set_bit(frame_head[0], 0)
        assert(len(message) < 126)
        frame_head[1] = len(message)
        frame = frame_head + message.encode('utf-8')
        return frame

    @staticmethod
    def decode_client_websocket_message(received_broadcast):
        """
        Helper to decode messages from the client side for testing purposes
        :param received_broadcast: the byte array received from the server
        :return: a decoded string
        """
        decoded_broadcast = ''
        if received_broadcast[0] == 129:
            for c in received_broadcast[2:]:
                decoded_broadcast += chr(c)
        return decoded_broadcast


    @staticmethod
    def set_bit(int_type, offset):
        """
        set_bit -- helper for bit operation
        :param int_type: the original value
        :param offset: which bit to set
        :return: the modified value
        """
        return int_type | (1 << offset)

    def finish(self):
        """
        finish is called when the connection is done
        """
        #print("finish:", self.client_address)
#        with self.server.lock:
#           self.server.remove_client(self)
        pass


class ThreadedWebSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    ThreadedWebSocketServer overrides the standard implementation to add a client list
    """
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, host_port, handler):
        super().__init__(host_port, handler)
        self.clients = {}
        self.lock = threading.Lock()

    def add_client(self, client):
        """
        add_client inserts a reference to the client handler object into the server's list of clients
        :param client: reference to the client handler
        """
        with self.lock:
            self.clients[client.client_address] = client
        #print("added: ", client.client_address)
        #print(self.clients.keys())

    def remove_client(self, client):
        """
        remove_client is called by the client handler when the client disconnects
        :param client: reference to the client handler
        """
        with self.lock:
            if client.client_address in self.clients.keys():
                self.clients.pop(client.client_address)
                #print("removed: ", client.client_address)

    def send_to_all_clients(self, msg):
        """
        send_to_all_clients sends the same message to all the connected clients
        :param msg: string to be sent to all connected clients
        """
        #print('send_to_all_clients')
        #print(self.clients.keys())
        with self.lock:
            for client in self.clients.values():
                #print("send_to:", client.client_address)
                client.request.send(ThreadedWebSocketHandler.encode_websocket_message(msg))


class WebSocketManager():
    """
    WebSocketManager implements the external interface to the WebSocket engine
    """

    def __init__(self):
        self.server = None
        self.server_thread = None

    def start(self):
        """
        start
        starts the WebSocket engine
        """
        self.server = ThreadedWebSocketServer((HOST, PORT), ThreadedWebSocketHandler)
        self.server_thread = socketserver.threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        #print("started the WebSocket server")

    def stop(self):
        """
        stop
        stops the WebSocket engine
        """
        self.server.shutdown()
        self.server.server_close()
        #print("stopped the WebSocket server")

    def send(self, msg):
        """
        sends a message to all clients via the websocket server
        :param msg: string to send
        """
        #print(self.server.clients.keys())
        self.server.send_to_all_clients(msg)

if __name__ == "__main__":
    #   The following code is helpful to test the server using a browser
    #   Just paste the following code into an html file
    #<html>
    #<head>
    #<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    #</head>
    #<body>
    #   <div id="results">start:</div>
    #</body>
    #<script type="text/javascript">
    #   appendMessage("testing...");
    #   var ws = new WebSocket('ws://localhost:8888/Pres')
    #   ws.onmessage = function(e){
    #	    appendMessage(e.data)
	#   }
    #   ws.onopen = function(){
	#       appendMessage("open");
	#       this.send("test send");
    #   }
    #   ws.onclose = function(){
	#       appendMessage("closed");
    #   }
    #   function appendMessage(str)
    #   {
    #       $("#results").html($("#results").html() + "<br />" + str);
    #   }
    #</script>
    #</html>

    manager = WebSocketManager()
    manager.start()
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Fake a handshake
    uid = uuid.uuid4()
    key = base64.encodebytes(uid.bytes).strip()
    data = ('\r\n'.join(WEB_SOCKET_CLIENT_HEADERS).format(host='localhost', port='8888', key=key)).encode('utf-8')
    received = None
    try:
        # Connect to server and send data
        sock.connect(('localhost', PORT))
        sock.send(data)
        received = sock.recv(1024)
        time.sleep(5)
        manager.send("broadcast")
        print("received: ", ThreadedWebSocketHandler.decode_client_websocket_message(sock.recv(1024)))
        time.sleep(2)
        manager.send("\r\njust before kill")
        print("received: ", ThreadedWebSocketHandler.decode_client_websocket_message(sock.recv(1024)))
        time.sleep(2)
    finally:
        sock.close()
        manager.stop()

