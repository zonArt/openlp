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

from PyQt4 import QtCore

from openlp.core.lib import Receiver

log = logging.getLogger(__name__)

class Controller(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    log.info(u'Controller loaded')

    def __init__(self, live):
        self.isLive = live
        self.doc = None
        log.info(u'%s controller loaded' % live)

    def addHandler(self, controller, file,  isBlank):
        log.debug(u'Live = %s, addHandler %s' % (self.isLive, file))
        self.controller = controller
        if self.doc is not None:
            self.shutdown()
        self.doc = self.controller.add_doc(file)
        self.doc.load_presentation()
        if self.isLive:
            self.doc.start_presentation()
            if isBlank:
                self.blank()
            Receiver.send_message(u'maindisplay_hide')
        self.doc.slidenumber = 0

    def activate(self):
        log.debug(u'Live = %s, activate' % self.isLive)
        if self.doc.is_active():
            return
        if not self.doc.is_loaded():
            self.doc.load_presentation()
        if self.isLive:
            self.doc.start_presentation()
            if self.doc.slidenumber > 1:
                self.doc.goto_slide(self.doc.slidenumber)

    def slide(self, slide, live):
        log.debug(u'Live = %s, slide' % live)
        if not live:
            return
        if self.doc.is_blank():
            self.doc.slidenumber = int(slide) + 1
            return
        self.activate()
        self.doc.goto_slide(int(slide) + 1)
        self.doc.poll_slidenumber(live)

    def first(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, first' % self.isLive)
        if not self.isLive:
            return
        if self.doc.is_blank():
            self.doc.slidenumber = 1
            return
        self.activate()
        self.doc.start_presentation()
        self.doc.poll_slidenumber(self.isLive)

    def last(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, last' % self.isLive)
        if not self.isLive:
            return
        if self.doc.is_blank():
            self.doc.slidenumber = self.doc.get_slide_count()
            return
        self.activate()
        self.doc.goto_slide(self.doc.get_slide_count())
        self.doc.poll_slidenumber(self.isLive)

    def next(self):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        log.debug(u'Live = %s, next' % self.isLive)
        if not self.isLive:
            return
        if self.doc.is_blank():
            if self.doc.slidenumber < self.doc.get_slide_count():
                self.doc.slidenumber = self.doc.slidenumber + 1
            return
        self.activate()
        self.doc.next_step()
        self.doc.poll_slidenumber(self.isLive)

    def previous(self):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        log.debug(u'Live = %s, previous' % self.isLive)
        if not self.isLive:
            return
        if self.doc.is_blank():
            if self.doc.slidenumber > 1:
                self.doc.slidenumber = self.doc.slidenumber - 1
            return
        self.activate()
        self.doc.previous_step()
        self.doc.poll_slidenumber(self.isLive)

    def shutdown(self):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        log.debug(u'Live = %s, shutdown' % self.isLive)
        if self.isLive:
            Receiver.send_message(u'maindisplay_show')
        self.doc.close_presentation()
        self.doc = None
        #self.doc.slidenumber = 0
        #self.timer.stop()

    def blank(self):
        log.debug(u'Live = %s, blank' % self.isLive)
        if not self.isLive:
            return
        if not self.doc.is_loaded():
            return
        if not self.doc.is_active():
            return
        self.doc.blank_screen()

    def unblank(self):
        log.debug(u'Live = %s, unblank' % self.isLive)
        if not self.isLive:
            return
        self.activate()
        if self.doc.slidenumber and self.doc.slidenumber != self.doc.get_slide_number():
            self.doc.goto_slide(self.doc.slidenumber)
        self.doc.unblank_screen()

    def poll(self):
        self.doc.poll_slidenumber(self.isLive)

class MessageListener(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    log.info(u'Message Listener loaded')

    def __init__(self, mediaitem):
        self.controllers = mediaitem.controllers
        self.mediaitem = mediaitem
        self.previewHandler = Controller(False)
        self.liveHandler = Controller(True)
        # messages are sent from core.ui.slidecontroller
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_stop'), self.shutdown)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_first'), self.first)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_previous'), self.previous)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_next'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_last'), self.last)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_slide'), self.slide)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_blank'), self.blank)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentation_unblank'), self.unblank)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        isLive, item = self.decode_message(message)
        log.debug(u'Startup called with message %s' % message)
        isBlank = message[2]
        file = os.path.join(item.get_frame_path(), 
            item.get_frame_title())
        self.handler = item.title
        if self.handler == self.mediaitem.Automatic:
            self.handler = self.mediaitem.findControllerByType(file)
            if not self.handler:
                return
        if isLive:
            controller = self.liveHandler
        else:
            controller = self.previewHandler
        controller.addHandler(self.controllers[self.handler], file, isBlank)

    def decode_message(self, message):
        return message[1], message[0]
        
    def slide(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.slide(slide, live)
        else:
            self.previewHandler.slide(slide, live)

    def first(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.first()
        else:
            self.previewHandler.first()

    def last(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.last()
        else:
            self.previewHandler.last()

    def next(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.next()
        else:
            self.previewHandler.next()

    def previous(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.previous()
        else:
            self.previewHandler.previous()

    def shutdown(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            Receiver.send_message(u'maindisplay_show')
            self.liveHandler.shutdown()
        else:
            self.previewHandler.shutdown()

    def blank(self, message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.blank()

    def unblank(self,  message):
        isLive, item = self.decode_message(message)
        if isLive:
            self.liveHandler.unblank()
        
    def timeout(self):
        self.liveHandler.poll()
        
