# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Tim Bentley, Jonathan Corwin, Michael      #
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
        self.handler = None
        self.is_live = None
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
        log.debug(u'startup %s ' % message)
        self.handler, file, self.is_live = self.decodeMessage(message)
        self.controller = self.controllers[self.handler]
        if self.controller.is_loaded():
            self.shutdown(None)
        print "aaa ", self.is_live
        self.controller.load_presentation(file)
        if self.is_live:
            self.controller.start_presentation()
            Receiver.send_message(u'live_slide_hide')
        self.controller.slidenumber = 0
        self.timer.start()

    def activate(self):
        log.debug(u'activate')
        if self.controller.is_active():
            return
        if not self.controller.is_loaded():
            self.controller.load_presentation(self.controller.filepath)
        log.debug(u'activate 2')
        print "activate 2"
        self.controller.start_presentation()
        log.debug(u'activate 3')
        print "activate 3"
        if self.controller.slidenumber > 1:
            self.controller.goto_slide(self.controller.slidenumber)

    def slide(self, message):
        log.debug(u'slide %s ' % message)
        #Not wanted for preview frame
        if not self.is_live:
            return
        slide, live = self.splitMessage(message)
        self.activate()
        print ">>> ", message
        if message:
            print message[0], self.is_live
            self.controller.goto_slide(int(slide) + 1)
            self.controller.poll_slidenumber(self.is_live)

    def first(self, message):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'first %s ' % message)
        #Not wanted for preview frame
        if not self.is_live:
            return
        self.activate()
        self.controller.start_presentation()
        self.controller.poll_slidenumber(self.is_live)

    def last(self, message):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'last %s ' % message)
        #Not wanted for preview frame
        if not self.is_live:
            return
        self.activate()
        self.controller.goto_slide(self.controller.get_slide_count())
        self.controller.poll_slidenumber(self.is_live)

    def next(self, message):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        log.debug(u'next ', message)
        #Not wanted for preview frame
        if not self.is_live:
            return
        self.activate()
        self.controller.next_step()
        self.controller.poll_slidenumber(self.is_live)

    def previous(self, message):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        log.debug(u'previous %s' % message)
        if not self.is_live:
            return
        self.activate()
        self.controller.previous_step()
        self.controller.poll_slidenumber(self.is_live)

    def shutdown(self, message):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        log.debug(u'shutdown %s ' % message)
        if self.is_live:
            Receiver.send_message(u'live_slide_show')
        self.controller.close_presentation()
        self.controller.slidenumber = 0
        self.timer.stop()

    def blank(self):
        log.debug(u'blank')
        if not self.is_live:
            return
        if not self.controller.is_loaded():
            return
        if not self.controller.is_active():
            return
        self.controller.blank_screen()

    def unblank(self):
        log.debug(u'unblank')
        if not self.is_live:
            return
        self.activate()
        self.controller.unblank_screen()

    def decodeMessage(self, message):
        """
        Splits the message from the SlideController into it's component parts

        ``message``
        Message containing Presentaion handler name and file to be presented.
        """
        file = os.path.join(message[1], message[2])
        return message[0], file, message[4]

    def timeout(self):
        self.controller.poll_slidenumber(self.is_live)

    def splitMessage(self, message):
        """
        Splits the selection messages
        into it's component parts

        ``message``
        Message containing Presentaion handler name and file to be presented.
        """
        bits = message.split(u':')
        return bits[0], bits[1]
