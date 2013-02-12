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
    This is the Component Registry.  It is a singleton object and is used to provide a
    look up service for common objects.
    """
    log.info(u'Registry loaded')
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
        log.info(u'Registry Initialising')
        registry = cls()
        registry.service_list = {}
        registry.running_under_test = False
        # Allow the tests to remove Registry entries but not the live system
        if u'nosetest' in sys.argv[0]:
            registry.running_under_test = True
        return registry

    def get(self, key):
        """
        Extracts the registry value from the list based on the key passed in
        """
        if key in self.service_list:
            return self.service_list[key]
        else:
            log.error(u'Service %s not found in list' % key)
            raise KeyError(u'Service %s not found in list' % key)

    def register(self, key, reference):
        """
        Registers a component against a key.
        """
        if key in self.service_list:
            log.error(u'Duplicate service exception %s' % key)
            raise KeyError(u'Duplicate service exception %s' % key)
        else:
            self.service_list[key] = reference

    def remove(self, key):
        """
        Removes the registry value from the list based on the key passed in
        (Only valid and active for testing framework)
        """
        if self.running_under_test is False:
            log.error(u'Invalid Method call for key %s' % key)
            raise KeyError(u'Invalid Method call for key %s' % key)
            return
        if key in self.service_list:
            del self.service_list[key]
