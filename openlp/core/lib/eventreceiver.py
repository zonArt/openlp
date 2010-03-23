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

from PyQt4 import QtCore

log = logging.getLogger(__name__)

class EventReceiver(QtCore.QObject):
    """
    Class to allow events to be passed from different parts of the
    system. This is a private class and should not be used directly
    but rather via the Receiver class.

    ``stop_import``
        Stops the Bible Import

    ``pre_load_bibles``
        Triggers the plugin to relaod the bible lists

    ``process_events``
        Requests the Application to flush the events queue

    ``{plugin}_add_service_item``
        ask the plugin to push the selected items to the service item

    ``update_themes``
        send out message with new themes

    ``update_global_theme``
        Tell the components we have a new global theme

    ``load_song_list``
        Tells the the song plugin to reload the song list

    ``load_custom_list``
        Tells the the custom plugin to reload the custom list

    ``update_spin_delay``
        Pushes out the Image loop delay

    ``request_spin_delay``
        Requests a spin delay

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

    ``{plugin}_stop``
        Requests a plugin to handle a stop event

    ``{plugin}_edit``
        Requests a plugin edit a database item with the key as the payload

    ``songusage_live``
        Sends live song audit requests to the audit component

    ``audit_changed``
        Audit information may have changed

    ``config_updated``
        Informs components the config has changed

    ``preview_song``
        Tells the song plugin the edit has finished and the song can be previewed
        Only available if the edit was triggered by the Preview button.

    ``slidecontroller_change``
        Informs the slidecontroller that a slide change has occurred

    ``remote_edit_clear``
        Informs all components that remote edit has been aborted.

    ``presentation types``
        Informs all components of the presentation types supported.

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


class Receiver():
    """
    Class to allow events to be passed from different parts of the system. This
    is a static wrapper around the ``EventReceiver`` class. As there is only
    one instance of it in the system the Qt4 signal/slot architecture can send
    messages across the system.

    To send a message:
       ``Receiver.send_message(u'<<Message ID>>', data)``

    To receive a Message
        ``QtCore.QObject.connect(Receiver.get_receiver(), QtCore.SIGNAL(u'<<Message ID>>'), <<ACTION>>)``
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

