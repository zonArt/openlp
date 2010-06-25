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
from openlp.core.ui import HideMode

log = logging.getLogger(__name__)

class Controller(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    log.info(u'Controller loaded')

    def __init__(self, live):
        self.is_live = live
        self.doc = None
        log.info(u'%s controller loaded' % live)

    def add_handler(self, controller, file, is_blank):
        log.debug(u'Live = %s, add_handler %s' % (self.is_live, file))
        self.controller = controller
        if self.doc is not None:
            self.shutdown()
        self.doc = self.controller.add_doc(file)
        self.doc.load_presentation()
        if self.is_live:
            self.doc.start_presentation()
            if is_blank:
                self.blank()
            Receiver.send_message(u'maindisplay_hide', HideMode.Screen)
        self.doc.slidenumber = 0

    def activate(self):
        log.debug(u'Live = %s, activate' % self.is_live)
        if self.doc.is_active():
            return
        if not self.doc.is_loaded():
            self.doc.load_presentation()
        if self.is_live:
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
        log.debug(u'Live = %s, first' % self.is_live)
        if not self.is_live:
            return
        if self.doc.is_blank():
            self.doc.slidenumber = 1
            return
        self.activate()
        self.doc.start_presentation()
        self.doc.poll_slidenumber(self.is_live)

    def last(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, last' % self.is_live)
        if not self.is_live:
            return
        if self.doc.is_blank():
            self.doc.slidenumber = self.doc.get_slide_count()
            return
        self.activate()
        self.doc.goto_slide(self.doc.get_slide_count())
        self.doc.poll_slidenumber(self.is_live)

    def next(self):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        log.debug(u'Live = %s, next' % self.is_live)
        if not self.is_live:
            return
        if self.doc.is_blank():
            if self.doc.slidenumber < self.doc.get_slide_count():
                self.doc.slidenumber = self.doc.slidenumber + 1
            return
        self.activate()
        self.doc.next_step()
        self.doc.poll_slidenumber(self.is_live)

    def previous(self):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        log.debug(u'Live = %s, previous' % self.is_live)
        if not self.is_live:
            return
        if self.doc.is_blank():
            if self.doc.slidenumber > 1:
                self.doc.slidenumber = self.doc.slidenumber - 1
            return
        self.activate()
        self.doc.previous_step()
        self.doc.poll_slidenumber(self.is_live)

    def shutdown(self):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        log.debug(u'Live = %s, shutdown' % self.is_live)
        if self.is_live:
            Receiver.send_message(u'maindisplay_show')
        self.doc.close_presentation()
        self.doc = None
        #self.doc.slidenumber = 0
        #self.timer.stop()

    def blank(self):
        log.debug(u'Live = %s, blank' % self.is_live)
        if not self.is_live:
            return
        if not self.doc.is_loaded():
            return
        if not self.doc.is_active():
            return
        self.doc.blank_screen()

    def stop(self):
        log.debug(u'Live = %s, stop' % self.is_live)
        if not self.is_live:
            return
        if not self.doc.is_loaded():
            return
        if not self.doc.is_active():
            return
        self.doc.stop_presentation()

    def unblank(self):
        log.debug(u'Live = %s, unblank' % self.is_live)
        if not self.is_live:
            return
        self.activate()
        if self.doc.slidenumber and \
            self.doc.slidenumber != self.doc.get_slide_number():
            self.doc.goto_slide(self.doc.slidenumber)
        self.doc.unblank_screen()
        Receiver.send_message(u'maindisplay_hide', HideMode.Screen)

    def poll(self):
        self.doc.poll_slidenumber(self.is_live)

class MessageListener(object):
    """
    This is the Presentation listener who acts on events from the slide
    controller and passes the messages on the the correct presentation handlers
    """
    log.info(u'Message Listener loaded')

    def __init__(self, mediaitem):
        self.controllers = mediaitem.controllers
        self.mediaitem = mediaitem
        self.preview_handler = Controller(False)
        self.live_handler = Controller(True)
        # messages are sent from core.ui.slidecontroller
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_stop'), self.shutdown)
        QtCore.QObject.connect(Receiver.get_receiver(),
            QtCore.SIGNAL(u'presentations_hide'), self.hide)
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
        QtCore.QObject.connect(
            self.timer, QtCore.SIGNAL("timeout()"), self.timeout)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        is_live = message[1]
        item = message[0]
        log.debug(u'Startup called with message %s' % message)
        is_blank = message[2]
        file = os.path.join(item.get_frame_path(),
            item.get_frame_title())
        self.handler = item.title
        if self.handler == self.mediaitem.Automatic:
            self.handler = self.mediaitem.findControllerByType(file)
            if not self.handler:
                return
        if is_live:
            controller = self.live_handler
        else:
            controller = self.preview_handler
        controller.add_handler(self.controllers[self.handler], file, is_blank)

    def slide(self, message):
        is_live = message[1]
        slide = message[2]
        item = message[0]
        if is_live:
            self.live_handler.slide(slide, item)
        else:
            self.preview_handler.slide(slide, item)

    def first(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.first()
        else:
            self.preview_handler.first()

    def last(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.last()
        else:
            self.preview_handler.last()

    def next(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.next()
        else:
            self.preview_handler.next()

    def previous(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.previous()
        else:
            self.preview_handler.previous()

    def shutdown(self, message):
        is_live = message[1]
        if is_live:
            Receiver.send_message(u'maindisplay_show')
            self.live_handler.shutdown()
        else:
            self.preview_handler.shutdown()

    def hide(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.stop()

    def blank(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.blank()

    def unblank(self, message):
        is_live = message[1]
        if is_live:
            self.live_handler.unblank()

    def timeout(self):
        self.live_handler.poll()
