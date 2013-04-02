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
"""
Provide event handling code for OpenLP
"""
import logging

from PyQt4 import QtCore

log = logging.getLogger(__name__)


class EventReceiver(QtCore.QObject):
    """
    Class to allow events to be passed from different parts of the system. This
    is a private class and should not be used directly but rather via the
    Receiver class.

    **Mainwindow related and generic signals**

    ``mainwindow_status_text``
        Changes the bottom status bar text on the mainwindow.

    ``openlp_error_message``
        Displays a standalone Error Message.

    ``openlp_information_message``
        Displays a standalone Information Message.

    ``openlp_version_check``
        Version has changed so pop up window.

    ``openlp_stop_wizard``
        Stops a wizard before completion.

    **Setting related signals**

    ``config_updated``
        Informs components that the config has changed.

    ``config_screen_changed``
        The display monitor has been changed.

    **Slidecontroller signals**

    ``slidecontroller_{live|preview}_next``
        Moves to the next slide.

    ``slidecontroller_{live|preview}_next_noloop``
        Moves to the next slide without auto advance.

    ``slidecontroller_{live|preview}_previous``
        Moves to the previous slide.

    ``slidecontroller_{live|preview}_previous_noloop``
        Moves to the previous slide, without auto advance.

    ``slidecontroller_{live|preview}_set``
        Moves to a specific slide, by index.

    ``slidecontroller_{live|preview}_started``
        Broadcasts that an item has been made live/previewed.

    ``slidecontroller_{live|preview}_change``
        Informs the slidecontroller that a slide change has occurred and to
        update itself.

    ``slidecontroller_{live|preview}_changed``
        Broadcasts that the slidecontroller has changed the current slide.

    ``slidecontroller_{live|preview}_blank``
        Request that the output screen is blanked.

    ``slidecontroller_{live|preview}_unblank``
        Request that the output screen is unblanked.

    ``slidecontroller_live_spin_delay``
        Pushes out the loop delay.

    ``slidecontroller_update_slide_limits``
        Updates the slide_limits variable from the saved settings.

    ``slidecontroller_live_stop_loop``
        Stop the loop on the main display.

    **Display signals**

    ``update_display_css``
        CSS has been updated which needs to be changed on the main display.

    **Live Display signals**

    ``live_display_hide``
        Hide the live display.

    ``live_display_show``
        Return the live display.

    ``live_display_active``
        The live display has been made active.

    ``live_display_blank_check``
        Check to see if the blank display message is required.

    **Theme related singlas**

    ``theme_update_list``
        send out message with new themes.

    ``theme_update_global``
        Tell the components we have a new global theme.

    **Plugin specific signals**

    ``{plugin}_start``
        Requests a plugin to start a external program. Path and file have to
        be provided in the message.

    ``{plugin}_first``
        Requests a plugin to handle a first event.

    ``{plugin}_previous``
        Requests a plugin to handle a previous event.

    ``{plugin}_next``
        Requests a plugin to handle a next event.

    ``{plugin}_last``
        Requests a plugin to handle a last event.

    ``{plugin}_slide``
        Requests a plugin to handle a go to specific slide event.

    ``{plugin}_stop``
        Requests a plugin to handle a stop event.

    ``{plugin}_blank``
        Requests a plugin to handle a blank screen event.

    ``{plugin}_unblank``
        Requests a plugin to handle an unblank screen event.

    ``{plugin}_load_list``
        Tells the the plugin to reload the media manager list.

    ``{plugin}_preview``
        Tells the plugin it's item can be previewed.

    ``{plugin}_add_service_item``
        Ask the plugin to push the selected items to the service item.

    ``{plugin}_service_load``
        Ask the plugin to process an individual service item after it has been
        loaded.

    ``{plugin}_config_updated``
        The config has changed so tell the plugin about it.

    ``alerts_text``
        Displays an alert message.

    ``bibles_nobook``
        Attempt to find book resulted in no match.

    ``remotes_poll_request``
        Waits for openlp to do something "interesting" and sends a
        ``remotes_poll_response`` signal when it does.

    """
    def __init__(self):
        """
        Initialise the event receiver, calling the parent constructor.
        """
        QtCore.QObject.__init__(self)

    def send_message(self, event, msg=None):
        """
        Emit a Qt signal.

        ``event``
            The event to that was sent.

        ``msg``
            Defaults to *None*. The message to send with the event.
        """
        log.debug(u'Event %s passed with payload %s' % (event, msg))
        self.emit(QtCore.SIGNAL(event), msg)


class Receiver(object):
    """
    Class to allow events to be passed from different parts of the system. This
    is a static wrapper around the ``EventReceiver`` class. As there is only
    one instance of it in the system the Qt4 signal/slot architecture can send
    messages across the system.

    To send a message:
       ``Receiver.send_message(u'<<Message ID>>', data)``

    To receive a Message
        ``QtCore.QObject.connect(
            Receiver.get_receiver(),
            QtCore.SIGNAL(u'<<Message ID>>'),
            <<ACTION>>
        )``
    """
    __eventreceiver__ = EventReceiver()

    @staticmethod
    def send_message(event, msg=None):
        """
        Sends a message to the messaging system.

        ``event``
            The event to send.

        ``msg``
            Defaults to *None*. The message to send with the event.
        """
        Receiver.__eventreceiver__.send_message(event, msg)

    @staticmethod
    def get_receiver():
        """
        Get the global ``__eventreceiver__`` instance.
        """
        return Receiver.__eventreceiver__
