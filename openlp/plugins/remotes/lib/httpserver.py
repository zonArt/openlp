# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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

import logging
import os
import json
import urlparse

from PyQt4 import QtCore, QtNetwork

from openlp.core.lib import Receiver
from openlp.core.utils import AppLocation

log = logging.getLogger(__name__)

class HttpServer(object):
    """ 
    Ability to control OpenLP via a webbrowser
    e.g.  http://localhost:4316/send/slidecontroller_live_next
          http://localhost:4316/send/alerts_text?q=your%20alert%20text
    """
    def __init__(self, parent):
        """
        Initialise the httpserver, and start the server
        """
        log.debug(u'Initialise httpserver')
        self.parent = parent
        self.html_dir = os.path.join(
            AppLocation.get_directory(AppLocation.PluginsDir),
            u'remotes', u'html')
        self.connections = []
        self.current_item = None
        self.current_slide = None
        self.start_tcp()

    def start_tcp(self):
        """
        Start the http server, use the port in the settings default to 4316
        Listen out for slide and song changes so they can be broadcast to 
        clients. Listen out for socket connections
        """
        log.debug(u'Start TCP server')
        port = QtCore.QSettings().value(
            self.parent.settingsSection + u'/remote port',
            QtCore.QVariant(4316)).toInt()[0]
        self.server = QtNetwork.QTcpServer()
        self.server.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), 
            port)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_changed'), 
            self.slide_change)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'slidecontroller_live_started'), 
            self.item_change)
        QtCore.QObject.connect(self.server,
            QtCore.SIGNAL(u'newConnection()'), self.new_connection)
        log.debug(u'TCP listening on port %d' % port)

    def slide_change(self, row):
        """
        Slide change listener. Store the item and tell the clients
        """
        self.current_slide = row
        self.send_poll()

    def item_change(self, items):
        """
        Item (song) change listener. Store the slide and tell the clients
        """
        self.current_item = items[0].title
        self.send_poll()
                        
    def send_poll(self):
        """
        Tell the clients something has changed
        """
        Receiver.send_message(u'remotes_poll_response',
            {'slide': self.current_slide,
             'item': self.current_item})
        
    def new_connection(self):
        """
        A new http connection has been made. Create a client object to handle
        communication
        """
        log.debug(u'new http connection')
        socket = self.server.nextPendingConnection()
        if socket:
            self.connections.append(HttpConnection(self, socket))
    
    def close_connection(self, connection):
        """
        The connection has been closed. Clean up
        """
        log.debug(u'close http connection')
        self.connections.remove(connection)

    def close(self):
        """
        Close down the http server
        """
        log.debug(u'close http server')
        self.server.close()
        
class HttpConnection(object):
    """ 
    A single connection, this handles communication between the server
    and the client
    """
    def __init__(self, parent, socket):
        """
        Initialise the http connection. Listen out for socket signals
        """
        log.debug(u'Initialise HttpConnection: %s' % 
            socket.peerAddress().toString())
        self.socket = socket
        self.parent = parent
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'readyRead()'),
            self.ready_read)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'disconnected()'),
            self.disconnected)

    def ready_read(self):
        """
        Data has been sent from the client. Respond to it
        """
        log.debug(u'ready to read socket')
        if self.socket.canReadLine():
            data = unicode(self.socket.readLine())
            log.debug(u'received: ' + data)
            words = data.split(u' ')
            html = None
            if words[0] == u'GET':
                url = urlparse.urlparse(words[1])
                params = self.load_params(url.query)
                folders = url.path.split(u'/')
                if folders[1] == u'':
                    html = self.serve_file(u'')
                elif folders[1] == u'files':
                    html = self.serve_file(folders[2])
                elif folders[1] == u'send':
                    html = self.process_event(folders[2], params)
                elif folders[1] == u'request':
                    if self.process_request(folders[2], params):
                        return
            if html:
                html = self.get_200_ok() + html + u'\n'
            else:
                html = self.get_404_not_found()
            self.socket.write(html)
            self.close()

    def serve_file(self, filename):
        """
        Send a file to the socket. For now, just .html files
        and must be top level inside the html folder. 
        If subfolders requested return 404, easier for security for the present.

        Ultimately for i18n, this could first look for xx/file.html before
        falling back to file.html... where xx is the language, e.g. 'en'
        """
        log.debug(u'serve file request %s' % filename)
        if not filename:
            filename = u'index.html'
        if os.path.basename(filename) != filename:
            return None
        (fileroot, ext) = os.path.splitext(filename)
        if ext != u'.html':
            return None
        path = os.path.join(self.parent.html_dir, filename)
        try:
            f = open(path, u'rb')
        except:
            log.exception(u'Failed to open %s' % path)
            return None
        log.debug(u'Opened %s' % path)
        html = f.read()
        f.close()
        return html
                               
    def load_params(self, query):
        """
        Decode the query string parameters sent from the browser
        """
        params = urlparse.parse_qs(query)
        if not params:
            return None
        else:
            return params['q']        
        
    def process_event(self, event, params):
        """
        Send a signal to openlp to perform an action.
        Currently lets anything through. Later we should restrict and perform
        basic parameter checking, otherwise rogue clients could crash openlp
        """
        if params:
            Receiver.send_message(event, params)    
        else:                  
            Receiver.send_message(event)    
        return u'OK'

    def process_request(self, event, params):
        """
        Client has requested data. Send the signal and parameters for openlp
        to handle, then listen out for a corresponding _request signal
        which will have the data to return.
        For most event timeout after 10 seconds (i.e. incase the signal 
        recipient isn't listening) 
        remotes_poll_request is a special case, this is a ajax long poll which
        is just waiting for slide change/song change activity. This can wait
        longer (one minute)
        """
        if not event.endswith(u'_request'):
            return False
        self.event = event
        response = event.replace(u'_request', u'_response')
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(response), self.process_response)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        QtCore.QObject.connect(self.timer,
            QtCore.SIGNAL(u'timeout()'), self.timeout)
        if event == 'remotes_poll_request':
            self.timer.start(60000)
        else:
            self.timer.start(10000)
        if params:
            Receiver.send_message(event, params)    
        else:                  
            Receiver.send_message(event)    
        return True

    def process_response(self, data):
        """
        The recipient of a _request signal has sent data. Convert this to 
        json and return it to client
        """
        if not self.socket:
            return
        self.timer.stop()
        html = json.dumps(data)
        html = self.get_200_ok() + html + u'\n'
        self.socket.write(html)
        self.close()

    def get_200_ok(self):
        """
        Successful request. Send OK headers. Assume html for now. 
        """
        return u'HTTP/1.1 200 OK\r\n' + \
            u'Content-Type: text/html; charset="utf-8"\r\n' + \
            u'\r\n'

    def get_404_not_found(self):
        """
        Invalid url. Say so
        """
        return u'HTTP/1.1 404 Not Found\r\n'+ \
            u'Content-Type: text/html; charset="utf-8"\r\n' + \
            u'\r\n'

    def get_408_timeout(self):
        """
        A _request hasn't returned anything in the timeout period. 
        Return timeout
        """
        return u'HTTP/1.1 408 Request Timeout\r\n'
            
    def timeout(self):
        """
        Listener for timeout signal
        """
        if not self.socket:
            return
        html = self.get_408_timeout()
        self.socket.write(html)
        self.close()
                
    def disconnected(self):
        """
        The client has disconnected. Tidy up
        """
        log.debug(u'socket disconnected')
        self.close()
                    
    def close(self):
        """
        The server has closed the connection. Tidy up
        """
        if not self.socket:
            return
        log.debug(u'close socket')
        self.socket.close()
        self.socket = None
        self.parent.close_connection(self)

