# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
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

import logging

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
        """
        Constructor
        """
        self.is_live = live
        self.doc = None
        self.hide_mode = None
        log.info(u'%s controller loaded' % live)

    def add_handler(self, controller, file, hide_mode, slide_no):
        """
        Add a handler, which is an instance of a presentation and
        slidecontroller combination. If the slidecontroller has a display
        then load the presentation.
        """
        log.debug(u'Live = %s, add_handler %s' % (self.is_live, file))
        self.controller = controller
        if self.doc is not None:
            self.shutdown()
        self.doc = self.controller.add_document(file)
        if not self.doc.load_presentation():
            # Display error message to user
            # Inform slidecontroller that the action failed?
            return
        self.doc.slidenumber = slide_no
        self.hide_mode = hide_mode
        if self.is_live:
            if hide_mode == HideMode.Screen:
                Receiver.send_message(u'live_display_hide', HideMode.Screen)
                self.stop()
            elif hide_mode == HideMode.Theme:
                self.blank(hide_mode)
            elif hide_mode == HideMode.Blank:
                self.blank(hide_mode)
            else:
                self.doc.start_presentation()
                Receiver.send_message(u'live_display_hide', HideMode.Screen)
                self.doc.slidenumber = 1
                if slide_no > 1:
                    self.slide(slide_no)

    def activate(self):
        """
        Active the presentation, and show it on the screen.
        Use the last slide number.
        """
        log.debug(u'Live = %s, activate' % self.is_live)
        if not self.doc:
            return False
        if self.doc.is_active():
            return True
        if not self.doc.is_loaded():
            if not self.doc.load_presentation():
                log.warn(u'Failed to activate %s' % self.doc.filepath)
                return False
        if self.is_live:
            self.doc.start_presentation()
            if self.doc.slidenumber > 1:
                if self.doc.slidenumber > self.doc.get_slide_count():
                    self.doc.slidenumber = self.doc.get_slide_count()
                self.doc.goto_slide(self.doc.slidenumber)
        if self.doc.is_active():
            return True
        else:
            log.warn(u'Failed to activate %s' % self.doc.filepath)
            return False

    def slide(self, slide):
        """
        Go to a specific slide
        """
        log.debug(u'Live = %s, slide' % self.is_live)
        if not self.doc:
            return
        if not self.is_live:
            return
        if self.hide_mode:
            self.doc.slidenumber = int(slide) + 1
            self.poll()
            return
        if not self.activate():
            return
        self.doc.goto_slide(int(slide) + 1)
        self.poll()

    def first(self):
        """
        Based on the handler passed at startup triggers the first slide
        """
        log.debug(u'Live = %s, first' % self.is_live)
        if not self.doc:
            return
        if not self.is_live:
            return
        if self.hide_mode:
            self.doc.slidenumber = 1
            self.poll()
            return
        if not self.activate():
            return
        self.doc.start_presentation()
        self.poll()

    def last(self):
        """
        Based on the handler passed at startup triggers the last slide
        """
        log.debug(u'Live = %s, last' % self.is_live)
        if not self.doc:
            return
        if not self.is_live:
            return
        if self.hide_mode:
            self.doc.slidenumber = self.doc.get_slide_count()
            self.poll()
            return
        if not self.activate():
            return
        self.doc.goto_slide(self.doc.get_slide_count())
        self.poll()

    def next(self):
        """
        Based on the handler passed at startup triggers the next slide event
        """
        log.debug(u'Live = %s, next' % self.is_live)
        if not self.doc:
            return
        if not self.is_live:
            return
        if self.hide_mode:
            if not self.doc.is_active():
                return
            if self.doc.slidenumber < self.doc.get_slide_count():
                self.doc.slidenumber += 1
                self.poll()
            return
        if not self.activate():
            return
        # The "End of slideshow" screen is after the last slide
        # Note, we can't just stop on the last slide, since it may
        # contain animations that need to be stepped through.
        if self.doc.slidenumber > self.doc.get_slide_count():
            return
        self.doc.next_step()
        self.poll()

    def previous(self):
        """
        Based on the handler passed at startup triggers the previous slide event
        """
        log.debug(u'Live = %s, previous' % self.is_live)
        if not self.doc:
            return
        if not self.is_live:
            return
        if self.hide_mode:
            if not self.doc.is_active():
                return
            if self.doc.slidenumber > 1:
                self.doc.slidenumber -= 1
                self.poll()
            return
        if not self.activate():
            return
        self.doc.previous_step()
        self.poll()

    def shutdown(self):
        """
        Based on the handler passed at startup triggers slide show to shut down
        """
        log.debug(u'Live = %s, shutdown' % self.is_live)
        if not self.doc:
            return
        self.doc.close_presentation()
        self.doc = None

    def blank(self, hide_mode):
        """
        Instruct the controller to blank the presentation
        """
        log.debug(u'Live = %s, blank' % self.is_live)
        self.hide_mode = hide_mode
        if not self.doc:
            return
        if not self.is_live:
            return
        if hide_mode == HideMode.Theme:
            if not self.doc.is_loaded():
                return
            if not self.doc.is_active():
                return
            Receiver.send_message(u'live_display_hide', HideMode.Theme)
        elif hide_mode == HideMode.Blank:
            if not self.activate():
                return
            self.doc.blank_screen()

    def stop(self):
        """
        Instruct the controller to stop and hide the presentation
        """
        log.debug(u'Live = %s, stop' % self.is_live)
        self.hide_mode = HideMode.Screen
        if not self.doc:
            return
        if not self.is_live:
            return
        if not self.doc.is_loaded():
            return
        if not self.doc.is_active():
            return
        self.doc.stop_presentation()

    def unblank(self):
        """
        Instruct the controller to unblank the presentation
        """
        log.debug(u'Live = %s, unblank' % self.is_live)
        self.hide_mode = None
        if not self.doc:
            return
        if not self.is_live:
            return
        if not self.activate():
            return
        if self.doc.slidenumber and self.doc.slidenumber != self.doc.get_slide_number():
            self.doc.goto_slide(self.doc.slidenumber)
        self.doc.unblank_screen()
        Receiver.send_message(u'live_display_hide', HideMode.Screen)

    def poll(self):
        if not self.doc:
            return
        self.doc.poll_slidenumber(self.is_live, self.hide_mode)


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
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_start'), self.startup)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_stop'), self.shutdown)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_hide'), self.hide)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_first'), self.first)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_previous'), self.previous)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_next'), self.next)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_last'), self.last)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_slide'), self.slide)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_blank'), self.blank)
        QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'presentations_unblank'), self.unblank)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL(u'timeout()'), self.timeout)

    def startup(self, message):
        """
        Start of new presentation
        Save the handler as any new presentations start here
        """
        is_live = message[1]
        item = message[0]
        log.debug(u'Startup called with message %s' % message)
        hide_mode = message[2]
        file = item.get_frame_path()
        self.handler = item.title
        if self.handler == self.mediaitem.Automatic:
            self.handler = self.mediaitem.findControllerByType(file)
            if not self.handler:
                return
        if is_live:
            controller = self.live_handler
        else:
            controller = self.preview_handler
        controller.add_handler(self.controllers[self.handler], file, hide_mode, message[3])

    def slide(self, message):
        """
        React to the message to move to a specific slide
        """
        is_live = message[1]
        slide = message[2]
        if is_live:
            self.live_handler.slide(slide)
        else:
            self.preview_handler.slide(slide)

    def first(self, message):
        """
        React to the message to move to the first slide
        """
        is_live = message[1]
        if is_live:
            self.live_handler.first()
        else:
            self.preview_handler.first()

    def last(self, message):
        """
        React to the message to move to the last slide
        """
        is_live = message[1]
        if is_live:
            self.live_handler.last()
        else:
            self.preview_handler.last()

    def next(self, message):
        """
        React to the message to move to the next animation/slide
        """
        is_live = message[1]
        if is_live:
            self.live_handler.next()
        else:
            self.preview_handler.next()

    def previous(self, message):
        """
        React to the message to move to the previous animation/slide
        """
        is_live = message[1]
        if is_live:
            self.live_handler.previous()
        else:
            self.preview_handler.previous()

    def shutdown(self, message):
        """
        React to message to shutdown the presentation. I.e. end the show
        and close the file
        """
        is_live = message[1]
        if is_live:
            self.live_handler.shutdown()
        else:
            self.preview_handler.shutdown()

    def hide(self, message):
        """
        React to the message to show the desktop
        """
        is_live = message[1]
        if is_live:
            self.live_handler.stop()

    def blank(self, message):
        """
        React to the message to blank the display
        """
        is_live = message[1]
        hide_mode = message[2]
        if is_live:
            self.live_handler.blank(hide_mode)

    def unblank(self, message):
        """
        React to the message to unblank the display
        """
        is_live = message[1]
        if is_live:
            self.live_handler.unblank()

    def timeout(self):
        """
        The presentation may be timed or might be controlled by the
        application directly, rather than through OpenLP. Poll occasionally
        to check which slide is currently displayed so the slidecontroller
        view can be updated
        """
        self.live_handler.poll()
