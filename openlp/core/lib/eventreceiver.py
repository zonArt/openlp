# -*- coding: utf-8 -*-
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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

from PyQt4.QtCore import *

class EventReceiver(QObject):
    """
    Class to allow events to be passed from different parts of the system.
    This is a private class and should not be used directly but via the Receiver class
    """
    def __init__(self):
        QObject.__init__(self)        
        
    def send_repaint(self):
        self.emit(SIGNAL("openlprepaint"), None)
        
    def received(self, msg=None):
        print msg
        
class Receiver():
    """
    Class to allow events to be passed from different parts of the system.
    This is a static wrapper arounf the EventReceiver class.
    As there is only one instance of it in the systems the QT signal/slot architecture
    can send messages across the system
    Send message
       receiver = Receiver()
       receiver.send_repaint()   
       
    Receive Message
        self.receiver = Receiver()
        QtCore.QObject.connect(self.receiver.get_receiver(),QtCore.SIGNAL("openlprepaint"),<<ACTION>>) 
    """    
    eventreceiver=EventReceiver()    
    @staticmethod
    def send_repaint():
        Receiver.eventreceiver.send_repaint()
    @staticmethod
    def receive():
        Receiver.eventreceiver.receive()
    @staticmethod        
    def get_receiver():
        return Receiver.eventreceiver
        
