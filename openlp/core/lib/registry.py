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
Provide Registry Services
"""
import logging
import sys

log = logging.getLogger(__name__)


class Registry(object):
    """
    This is the Component Registry.  It is a singleton object and is used to provide a look up service for common
    objects.
    """
    log.info('Registry loaded')
    __instance__ = None

    def __new__(cls):
        """
        Re-implement the __new__ method to make sure we create a true singleton.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    @classmethod
    def create(cls):
        """
        The constructor for the component registry providing a single registry of objects.
        """
        log.info('Registry Initialising')
        registry = cls()
        registry.service_list = {}
        registry.functions_list = {}
        registry.running_under_test = False
        # Allow the tests to remove Registry entries but not the live system
        if 'nose' in sys.argv[0]:
            registry.running_under_test = True
        return registry

    def get(self, key):
        """
        Extracts the registry value from the list based on the key passed in

        ``key``
            The service to be retrieved.
        """
        if key in self.service_list:
            return self.service_list[key]
        else:
            log.error('Service %s not found in list' % key)
            raise KeyError('Service %s not found in list' % key)

    def register(self, key, reference):
        """
        Registers a component against a key.

        ``key``
            The service to be created this is usually a major class like "renderer" or "main_window" .

        ``reference``
            The service address to be saved.
        """
        if key in self.service_list:
            log.error('Duplicate service exception %s' % key)
            raise KeyError('Duplicate service exception %s' % key)
        else:
            self.service_list[key] = reference

    def remove(self, key):
        """
        Removes the registry value from the list based on the key passed in (Only valid and active for testing
        framework).

        ``key``
            The service to be deleted.
        """
        if key in self.service_list:
            del self.service_list[key]

    def register_function(self, event, function):
        """
        Register an event and associated function to be called

        ``event``
            The function description like "live_display_hide" where a number of places in the code
            will/may need to respond to a single action and the caller does not need to understand or know about the
            recipients.

        ``function``
            The function to be called when the event happens.
        """
        if event in self.functions_list:
            self.functions_list[event].append(function)
        else:
            self.functions_list[event] = [function]

    def remove_function(self, event, function):
        """
        Remove an event and associated handler

        ``event``
            The function description..

        ``function``
            The function to be called when the event happens.
        """
        if self.running_under_test is False:
            log.error('Invalid Method call for key %s' % event)
            raise KeyError('Invalid Method call for key %s' % event)
        if event in self.functions_list:
            self.functions_list[event].remove(function)

    def execute(self, event, *args, **kwargs):
        """
        Execute all the handlers associated with the event and return an array of results.

        ``event``
            The function to be processed

        ``*args``
            Parameters to be passed to the function.

        ``*kwargs``
            Parameters to be passed to the function.
        """
        results = []
        if event in self.functions_list:
            for function in self.functions_list[event]:
                try:
                    result = function(*args, **kwargs)
                    if result:
                        results.append(result)
                except TypeError:
                    # Who has called me can help in debugging
                    import inspect
                    log.debug(inspect.currentframe().f_back.f_locals)
                    log.exception('Exception for function %s', function)
        return results
