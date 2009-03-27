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
import os
import logging

class EventManager(object):
    """
    A mechanism to send events to all registered endpoints
    the endpoints are registered and listen with a handle_event method
    the endpoint will decide whether to do somthing with the event or ignore it
    
    """
    global log
    log=logging.getLogger(u'EventManager')
    
    def __init__(self):
        self.endpoints=[]
        log.info(u'Initialising')
        
    def register(self, plugin):
        log.debug(u'plugin %s registered with EventManager'%plugin)        
        self.endpoints.append(plugin)
        
    def post_event(self, event):
        log.debug(u'post event called for event %s'%event.get_type)
        for point in self.endpoints:
            point.handle_event(event)

