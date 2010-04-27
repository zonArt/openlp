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
import json
import urlparse

from PyQt4 import QtCore, QtNetwork

from openlp.core.lib import Receiver

log = logging.getLogger(__name__)

class HttpServer(object):
    """ 
    Ability to control OpenLP via a webbrowser
    e.g.  http://localhost:4316/send/slidecontroller_live_next
          http://localhost:4316/send/alerts_text?q=your%20alert%20text
    """
    def __init__(self, parent):
        log.debug(u'Initialise httpserver')
        self.parent = parent
        self.connections = []
        self.start_tcp()

    def start_tcp(self):
        log.debug(u'Start TCP server')
        port = self.parent.config.get_config(u'remote port', 4316)
        self.server = QtNetwork.QTcpServer()
        self.server.listen(QtNetwork.QHostAddress(QtNetwork.QHostAddress.Any), 
            int(port))
        QtCore.QObject.connect(self.server,
            QtCore.SIGNAL(u'newConnection()'), self.new_connection)
        log.debug(u'TCP listening on port %s' % port)
            
    def new_connection(self):
        log.debug(u'new http connection')
        socket = self.server.nextPendingConnection()
        if socket:
            self.connections.append(HttpConnection(self, socket))
    
    def close_connection(self, connection):
        log.debug(u'close http connection')
        self.connections.remove(connection)

    def close(self):
        log.debug(u'close http server')
        self.server.close()
        
class HttpConnection(object):

    def __init__(self, parent, socket):
        log.debug(u'Initialise HttpConnection: %s' % 
            socket.peerAddress().toString())
        self.socket = socket
        self.parent = parent
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'readyRead()'),
            self.ready_read)
        QtCore.QObject.connect(self.socket, QtCore.SIGNAL(u'disconnected()'),
            self.disconnected)

    def ready_read(self):
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
                    html = self.process_index()
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
            
    def process_index(self):
        return u"""
<html>
<head>
<title>OpenLP Controller</title>
<script type='text/javascript'>

function send_event(eventname, data){
    var req = new XMLHttpRequest();
    url = 'send/' + eventname;
    if(data!=null)
        url += '?q=' + escape(data);
    req.open('GET', url, true);
    req.send();
}
function get_service(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if(req.readyState==4 && req.status==200){
            data = eval('(' + req.responseText + ')');
            html = '<table>';
            for(row in data){
                html += '<tr><td>' + data[row][0] + '</td></tr>';
            }
            html += '</table>';
            service = document.getElementById('service');
            service.innerHTML = html;        
        }        
    }
    req.open('GET', 'request/servicemanager_list_request', true);
    req.send();
}
</script>
</head>
<body>
    <h1>OpenLP Controller</h1>
    <input type='button' value='<- Previous Slide' onclick='send_event("slidecontroller_live_previous");'>
    <input type='button' value='Next Slide ->' onclick='send_event("slidecontroller_live_next");'>
    <br>
    <input type='button' value='<- Previous Item' onclick='send_event("servicemanager_previous_item");'>
    <input type='button' value='Next Item ->' onclick='send_event("servicemanager_next_item");'>
    <br>
    <label>Alert text</label><input id='alert' type='text'>
    <input type='button' value='Send' 
        onclick='send_event("alerts_text", 
        document.getElementById("alert").value);'>
    <br>
    <input type='button' value='Order of service' onclick='get_service();'>
    <div id='service'>
    </div>
</body>
</html>
"""
            
    def load_params(self, query):
        params = urlparse.parse_qs(query)
        if not params:
            return None
        else:
            return params['q']        
        
    def process_event(self, event, params):
        if params:
            Receiver.send_message(event, params)    
        else:                  
            Receiver.send_message(event)    
        return u'OK'

    def process_request(self, event, params):
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
        self.timer.start(10000)
        if params:
            Receiver.send_message(event, params)    
        else:                  
            Receiver.send_message(event)    
        return True

    def process_response(self, data):
        if not self.socket:
            return
        self.timer.stop()
        html = json.dumps(data)
        html = self.get_200_ok() + html + u'\n'
        self.socket.write(html)
        self.close()

    def get_200_ok(self):
        return u'HTTP/1.1 200 OK\r\n' + \
            u'Content-Type: text/html; charset="utf-8"\r\n' + \
            u'\r\n'

    def get_404_not_found(self):
        return u'HTTP/1.1 404 Not Found\r\n'+ \
            u'Content-Type: text/html; charset="utf-8"\r\n' + \
            u'\r\n'

    def get_408_timeout(self):
        return u'HTTP/1.1 408 Request Timeout\r\n'
            
    def timeout(self):
        if not self.socket:
            return
        html = self.get_408_timeout()
        self.socket.write(html)
        self.close()
                
    def disconnected(self):
        log.debug(u'socket disconnected')
        self.close()
                    
    def close(self):
        if not self.socket:
            return
        log.debug(u'close socket')
        self.socket.close()
        self.socket = None
        self.parent.close_connection(self)

