# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Maikel Stuivenberg, Martin Thompson, Jon Tibble,   #
# Carsten Tinggaard                                                           #
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

from PyQt4 import QtCore

from openlp.core.lib import Receiver

class Controller(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    global log
    log = logging.getLogger(u'Controller')
    log.info(u'Controller loaded')

    def __init__(self, live):
        self.isLive = live
        log.info(u'%s controller loaded' % live)

    def addHandler(self, controller, file):
        log.debug(u'Live = %s, addHandler %s' % (self.isLive, file))
        self.controller = controller
        if self.controller.is_loaded():
            self.shutdown()
        self.controller.load_presentation(file)
        if self.isLive:
            self.controller.start_presentation()
            Receiver.send_message(u'live_slide_hide')
        self.controller.slidenumber = 0

    def activate(self):
        log.debug(u'Live = %s, activate' % self.isLive)
        if self.controller.is_active():
            return
        if not self.controller.is_loaded():
            self.controller.load_presentation(self.controller.filepath)
        if self.isLive:
            self.controller.start_presentation()
            if self.controller.slidenumber > 1:
                self.controller.goto_slide(self.controller.slidenumber)

    def slide(self, slide, live):
        log.debug(u'Live = %s, slide' % live)
#        if not isLive:
#            return
        self.activate()
        self.controller.goto_slide(int(slide) + 1)
        self.controller.poll_slidenumber(live)

    def first(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, first' % self.isLive)
        if not self.isLive:
            return
        self.activate()
        self.controller.start_presentation()
        self.controller.poll_slidenumber(self.isLive)

    def last(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, last' % self.isLive)
        if not self.isLive:
            return
        self.activate()
        self.controller.goto_slide(self.controller.get_slide_count())
        self.controller.poll_slidenumber(self.isLive)

    def next(self):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        log.debug(u'Live = %s, next' % self.isLive)
        if not self.isLive:
            return
        self.activate()
        self.controller.next_step()
        self.controller.poll_slidenumber(self.isLive)

    def previous(self):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        log.debug(u'Live = %s, previous' % self.isLive)
        if not self.isLive:
            return
        self.activate()
        self.controller.previous_step()
        self.controller.poll_slidenumber(self.isLive)

    def shutdown(self):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        log.debug(u'Live = %s, shutdown' % self.isLive)
        self.controller.close_presentation()
        self.controller.slidenumber = 0
        #self.timer.stop()

    def blank(self):
        if not self.isLive:
            return
        if not self.controller.is_loaded():
            return
        if not self.controller.is_active():
            return
        self.controller.blank_screen()

    def unblank(self):
        if not self.is_live:
            return
        self.activate()
        self.controller.unblank_screen()


class MessageListener(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    global log
    log = logging.getLogger(u'MessageListener')
    log.info(u'Message Listener loaded')

    def __init__(self, controllers):
        self.controllers = controllers
        self.previewHandler = Controller(False)
        self.liveHandler = Controller(True)
        # messages are sent from core.ui.slidecontroller
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_stop'), self.shutdown)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_first'), self.first)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_previous'), self.previous)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_next'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_last'), self.last)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_slide'), self.slide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_blank'), self.blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_unblank'), self.unblank)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        log.debug(u'Startup called with message %s' % message)
        self.handler, file, isLive = self.decodeMessage(message)
        if isLive:
            self.liveHandler.addHandler(self.controllers[self.handler], file)
        else:
            self.previewHandler.addHandler(self.controllers[self.handler], file)

    def slide(self, message):
        slide, live = self.splitMessage(message)
        if live:
            self.liveHandler.slide(slide, live)
        else:
            self.previewHandler.slide(slide, live)

    def first(self, isLive):
        if isLive:
            self.liveHandler.first()
        else:
            self.previewHandler.first()

    def last(self, isLive):
        if isLive:
            self.liveHandler.last()
        else:
            self.previewHandler.last()

    def next(self, isLive):
        if isLive:
            self.liveHandler.next()
        else:
            self.previewHandler.next()

    def previous(self, isLive):
        if isLive:
            self.liveHandler.previous()
        else:
            self.previewHandler.previous()

    def shutdown(self, isLive):
        if isLive:
            self.liveHandler.shutdown()
            Receiver.send_message(u'live_slide_show')
        else:
            self.previewHandler.shutdown()

    def blank(self):
        if self.isLive:
            self.liveHandler.blank()
        else:
            self.previewHandler.blank()

    def unblank(self):
        if self.isLive:
            self.liveHandler.unblank()
        else:
            self.previewHandler.unblank()

    def splitMessage(self, message):
        """
        Splits the selection messages
        into it's component parts

        ``message``
        Message containing Presentaion handler name and file to be presented.
        """
        bits = message.split(u':')
        return bits[0], bits[1]

    def decodeMessage(self, message):
        """
        Splits the initial message from the SlideController
        into it's component parts

        ``message``
        Message containing Presentaion handler name and file to be presented.
        """
        file = os.path.join(message[1], message[2])
        return message[0], file, message[4]

    def timeout(self):
        self.controller.poll_slidenumber(self.is_live)
