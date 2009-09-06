# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley

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
import logging
import os

from PyQt4 import QtCore
from openlp.core.lib import Receiver
from openlp.plugins.presentations.lib import ImpressController

class MessageListener(object):
    """
    This is the Presentation listener who acts on events from the slide controller
    and passes the messages on the the correct presentation handlers
    """
    global log
    log=logging.getLogger(u'MessageListener')
    log.info(u'Message Listener loaded')

    def __init__(self, controllers):
        self.controllers = controllers
        self.handler = None

        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_stop'), self.shutDown)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_first'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_previous'), self.previous)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_next'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_last'), self.next)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        self.handler, file =  self.decodeMessage(message)
        self.controllers[self.handler].loadPresentation(file)

    def next(self, message):
        self.controllers[self.handler].nextStep()

    def previous(self, message):
        self.controllers[self.handler].previousStep()

    def shutDown(self, message):
        self.controllers[self.handler].closePresentation()

    def decodeMessage(self, message):
        bits = message.split(u':')
        file = os.path.join(bits[1], bits[2])
        return bits[0], file
