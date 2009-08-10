#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""
import sys
import logging
from PyQt4 import QtNetwork, QtGui, QtCore

logging.basicConfig(level=logging.DEBUG,
    format=u'%(asctime)s:%(msecs)3d %(name)-15s %(levelname)-8s %(message)s',
    datefmt=u'%m-%d %H:%M:%S', filename=u'openlp-cli.log', filemode=u'w')

class OpenLPRemoteCli():
    global log
    log = logging.getLogger(u'OpenLP Remote Application')
    log.info(u'Application Loaded')

    def __init__(self, argv):
        log.debug(u'Initialising')
        try:
            self.tcpsocket = QtNetwork.QUdpSocket()
            self.sendData()
        except:
            log.error(u'Errow thrown %s', sys.exc_info()[1])
            print u'Errow thrown ', sys.exc_info()[1]

    def sendData(self):
        text = "Alert:Wave to Zak, Superfly"
        print self.tcpsocket
        print self.tcpsocket.writeDatagram(text, QtNetwork.QHostAddress(QtNetwork.QHostAddress.Broadcast), 4316)

    def run(self):
        pass

if __name__ == u'__main__':
    app = OpenLPRemoteCli(sys.argv)
    app.run()

