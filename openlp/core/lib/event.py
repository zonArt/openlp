# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Scott Guerreri,
    Carsten Tingaard, Jonathan Corwin

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

class EventType(object):
    """
    Types of events are stored in this class.
    """
    # "Default" event - a non-event
    Default            = 0
    # General application events
    InitApplication    = -1
    ShowApplication    = -2
    BeforeAppClose     = -3
    ApplicationClose   = -4
    # Service events
    BeforeLoadService  = 1
    AfterLoadService   = 2
    BeforeSaveService  = 3
    AfterSaveService   = 4
    LoadServiceItem   = 5
    # Preview events
    PreviewShow  = 10
    LiveShow  = 11
    #PreviewBeforeLoad  = 11
    #PreviewAfterLoad   = 12
    #PreviewBeforeShow  = 13
    #PreviewAfterShow   = 14

    ThemeListChanged = 15


class Event(object):
    """
    Provides an Event class to encapsulate events within openlp.org.
    """
    def __init__(self, event_type=EventType.Default, payload=None):
        self.event_type = event_type
        self.payload = payload

    def get_type(self):
        return self.event_type
