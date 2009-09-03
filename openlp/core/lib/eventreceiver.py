# -*- coding: utf-8 -*-
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
import logging

from PyQt4 import QtCore

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

    ``update_spin_delay``
        Pushes out the Image loop delay

    ``request_spin_delay``
        Requests a spin delay

    """
    global log
    log = logging.getLogger(u'EventReceiver')

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
        self.emit(QtCore.SIGNAL(event), msg)


class Receiver():
    """
    Class to allow events to be passed from different parts of the
    system. This is a static wrapper around the ``EventReceiver``
    class. As there is only one instance of it in the system the QT
    signal/slot architecture can send messages across the system.

    To send a message:
       ``Receiver().send_message(u'<<Message ID>>', data)``

    To receive a Message
        ``QtCore.QObject.connect(Receiver().get_receiver(), QtCore.SIGNAL(u'<<Message ID>>'), <<ACTION>>)``
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


