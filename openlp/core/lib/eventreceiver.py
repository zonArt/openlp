# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Sam Scudder, Jeffrey Smith,      #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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
    Class to allow events to be passed from different parts of the
    system. This is a private class and should not be used directly
    but rather via the Receiver class.

    ``openlp_process_events``
        Requests the Application to flush the events queue

    ``openlp_version_check``
        Version has changed so pop up window.

    ``config_updated``
        Informs components the config has changed

    ``config_screen_changed``
        The display monitor has been changed

    ``slidecontroller_{live|preview}_first``
        Moves to the first slide

    ``slidecontroller_{live|preview}_next``
        Moves to the next slide

    ``slidecontroller_{live|preview}_next_noloop``
        Moves to the next slide without auto advance

    ``slidecontroller_{live|preview}_previous``
        Moves to the previous slide

    ``slidecontroller_{live|preview}_previous_noloop``
        Moves to the previous slide, without auto advance

    ``slidecontroller_{live|preview}_last``
        Moves to the last slide

    ``slidecontroller_{live|preview}_set``
        Moves to a specific slide, by index

    ``slidecontroller_{live|preview}_started``
        Broadcasts that an item has been made live/previewed

    ``slidecontroller_{live|preview}_change``
        Informs the slidecontroller that a slide change has occurred and to
        update itself

    ``slidecontroller_{live|preview}_changed``
        Broadcasts that the slidecontroller has changed the current slide

    ``slidecontroller_{live|preview}_text_request``
        Request the text for the current item in the controller
        Returns a slidecontroller_{live|preview}_text_response with an
        array of dictionaries with the tag and verse text

    ``slidecontroller_{live|preview}_blank``
        Request that the output screen is blanked

    ``slidecontroller_{live|preview}_unblank``
        Request that the output screen is unblanked

    ``slidecontroller_live_spin_delay``
        Pushes out the loop delay

    ``slidecontroller_live_stop_loop``
        Stop the loop on the main display

    ``servicemanager_previous_item``
        Display the previous item in the service

    ``servicemanager_preview_live``
        Requests a Preview item from the Service Manager to update live and
        add a new item to the preview panel

    ``servicemanager_next_item``
        Display the next item in the service

    ``servicemanager_set_item``
        Go live on a specific item, by index

    ``maindisplay_blank``
        Blank the maindisplay window

    ``maindisplay_hide``
        Hide the maindisplay window

    ``maindisplay_show``
        Return the maindisplay window

    ``maindisplay_active``
        The maindisplay has been made active

    ``maindisplay_status_text``
        Changes the bottom status bar text on the maindisplay window

    ``maindisplay_blank_check``
        Check to see if the blank display message is required

    ``videodisplay_start``
        Open a media item and prepare for playing

    ``videodisplay_play``
        Start playing a media item

    ``videodisplay_pause``
        Pause a media item

    ``videodisplay_stop``
        Stop playing a media item

    ``videodisplay_background``
        Replace the background video

    ``theme_update_list``
        send out message with new themes

    ``theme_update_global``
        Tell the components we have a new global theme

    ``{plugin}_start``
        Requests a plugin to start a external program
        Path and file provided in message

    ``{plugin}_first``
        Requests a plugin to handle a first event

    ``{plugin}_previous``
        Requests a plugin to handle a previous event

    ``{plugin}_next``
        Requests a plugin to handle a next event

    ``{plugin}_last``
        Requests a plugin to handle a last event

    ``{plugin}_slide``
        Requests a plugin to handle a go to specific slide event

    ``{plugin}_stop``
        Requests a plugin to handle a stop event

    ``{plugin}_blank``
        Requests a plugin to handle a blank screen event

    ``{plugin}_unblank``
        Requests a plugin to handle an unblank screen event

    ``{plugin}_edit``
        Requests a plugin edit a database item with the key as the payload

    ``{plugin}_edit_clear``
        Editing has been completed

    ``{plugin}_load_list``
        Tells the the plugin to reload the media manager list

    ``{plugin}_preview``
        Tells the plugin it's item can be previewed

    ``{plugin}_add_service_item``
        Ask the plugin to push the selected items to the service item

    ``{plugin}_service_load``
        Ask the plugin to process an individual service item after it has been
        loaded

    ``service_item_update``
        Passes back to the service manager the service item after it has been
        processed by the plugin

    ``alerts_text``
        Displays an alert message

    ``bibles_nobook``
        Attempt to find book resulted in no match

    ``openlp_stop_wizard``
        Stops a wizard before completion

    ``remotes_poll_request``
        Waits for openlp to do something "interesting" and sends a
        remotes_poll_response signal when it does

    ``openlp_warning_message``
        Displays a standalone Warning Message

    ``openlp_error_message``
        Displays a standalone Error Message

    ``openlp_information_message``
        Displays a standalone Information Message

    ``cursor_busy``
        Makes the cursor got to a busy form

    ``cursor_normal``
        Resets the cursor to default

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
    eventreceiver = EventReceiver()

    @staticmethod
    def send_message(event, msg=None):
        """
        Sends a message to the messaging system.

        ``event``
            The event to send.

        ``msg``
            Defaults to *None*. The message to send with the event.
        """
        Receiver.eventreceiver.send_message(event, msg)

    @staticmethod
    def get_receiver():
        """
        Get the global ``eventreceiver`` instance.
        """
        return Receiver.eventreceiver
